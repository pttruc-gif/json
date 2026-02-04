import pandas as pd
import json
import os
from pathlib import Path

# --- CẤU HÌNH ---
input_folder = '/home/npquy/DeepSeek-OCR/DeepSeek_OCR-master/Truc/Json'  # Thư mục chứa JSON
output_folder = '/home/npquy/DeepSeek-OCR/Truc/Excel_Output/' # Thư mục lưu Excel

# Tạo thư mục đầu ra nếu chưa có
os.makedirs(output_folder, exist_ok=True)

def convert_folder_json_to_excel():
    # Lấy danh sách file JSON
    json_files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    
    if not json_files:
        print(f"❌ Không tìm thấy file JSON nào trong: {input_folder}")
        return

    for filename in json_files:
        json_path = os.path.join(input_folder, filename)
        excel_name = filename.replace('.json', '.xlsx')
        excel_path = os.path.join(output_folder, excel_name)

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Chuyển đổi dữ liệu (đề, lời giải) thành DataFrame
            # Đảm bảo dữ liệu là danh sách để Pandas đọc đúng dòng/cột
            items = data if isinstance(data, list) else [data]
            df = pd.DataFrame(items)

            # BƯỚC QUAN TRỌNG: Ép kiểu toàn bộ DataFrame thành String 
            # để tránh Excel tự ý biến công thức toán thành lỗi #NAME?
            df = df.astype(str)

            # Xuất file Excel
            df.to_excel(excel_path, index=False)
            print(f"✅ Thành công: {filename} -> {excel_name}")
            
        except Exception as e:
            print(f"⚠️ Lỗi tại file {filename}: {e}")

if __name__ == "__main__":
    convert_folder_json_to_excel()
    print("\n🚀 Đã hoàn thành chuyển đổi toàn bộ thư mục!")