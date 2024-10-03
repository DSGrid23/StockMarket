import requests
import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Đọc file ticker.csv để lấy danh sách mã chứng khoán
file_path_ticker = 'ticker.csv'
ticker_data = pd.read_csv(file_path_ticker)

# Lấy các mã chứng khoán từ file CSV và lưu vào danh sách
ticker_list = ticker_data.iloc[:, 0].tolist()

# Tạo thư mục "Stock" nếu chưa tồn tại
os.makedirs('Stock', exist_ok=True)
os.makedirs('StockCSV', exist_ok=True)
def convert_to_csv(_file,folder):
    # Đọc file HTML
    with open(_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Tìm tất cả các bảng trong file HTML
    tables = soup.find_all("table")

    # Duyệt qua các bảng để lấy bảng mà bạn muốn
    # Giả sử bạn muốn lấy bảng thứ hai (tùy theo vị trí của bảng bạn cần)
    df = pd.read_html(str(tables[1]))[0]  # Bảng thứ 2
    file_name = os.path.basename(_file)
    base_name = os.path.splitext(file_name)[0]
    df.to_csv(os.path.join(folder, f"{base_name}.csv"), index=False)



# Hàm tải dữ liệu và lưu vào file với tên dựa trên mã chứng khoán và ngày hiện tại
def download_file_per_ticker(code, from_date="2021-01-01", to_date="2024-09-28", page_index=1, page_size=10):
    # URL tải file với placeholder cho giá trị code
    #url = f"https://finance.vietstock.vn/data/ExportTradingResult?Code={code}&OrderBy=&OrderDirection=desc&PageIndex={page_index}&PageSize={page_size}&FromDate={from_date}&ToDate={to_date}&ExportType=text&Cols=TKLGD%2CTGTGD%2CVHTT%2CTGG%2CDC%2CTGPTG%2CKLGDKL%2CGTGDKL&ExchangeID=5"
    url=f"https://finance.vietstock.vn/data/ExportTradingResult?Code={code}&OrderBy=&OrderDirection=desc&PageIndex={page_index}&PageSize={page_size}&FromDate={from_date}&ToDate={to_date}&ExportType=excel&Cols=KLNY%2CKLCPDLH%2CGTC%2CT%2CS%2CTKLGD%2CTGTGD%2CVHTT%2CMC%2CTGG%2CLDM%2CDC%2CTGPTG%2CLDB%2CCN%2CBQM%2CLDMB%2CTN%2CBQB%2CKLDM%2CGYG%2CDM%2CKLDB%2CBQ%2CDB%2CKLDMB%2CGDC%2CKLGDKL%2CGTGDKL%2CKLGDTT%2CGTGDTT&ExchangeID=5"
    # Thêm headers để giả lập trình duyệt
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
        'Referer': 'https://finance.vietstock.vn/ACV/thong-ke-giao-dich.htm',
    }
    
    # Tên file để lưu dữ liệu theo mã chứng khoán và ngày hiện tại, lưu trong thư mục "Stock"
    output_file = os.path.join('Stock', f"{code}_{to_date}.txt")

    # Gửi yêu cầu HTTP GET để tải file với headers
    response = requests.get(url, headers=headers, stream=True)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        # Ghi dữ liệu vào file
        with open(output_file, 'w', encoding='utf-8') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk.decode('utf-8', errors='ignore'))
        convert_to_csv(output_file,'StockCSV')
        print(f"Dữ liệu cho {code} đã được lưu vào file {output_file}.")
    else:
        print(f"Tải dữ liệu cho {code} thất bại. Mã trạng thái: {response.status_code}")

# Lặp qua từng mã chứng khoán và tải dữ liệu, lưu vào file trong thư mục "Stock"
for ticker in ticker_list:
    download_file_per_ticker(ticker)


# filename='Stock\ACB_2024-09-28.txt'
# fileneme_csv=filename.split('/')[1].split('.')[0]+'.csv'
# print(fileneme_csv)