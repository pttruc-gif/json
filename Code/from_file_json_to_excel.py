import pandas as pd
import json

def json_to_excel_raw(input_path, output_path):
    try:
        # 1. Đọc file JSON với mã hóa UTF-8
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. Phẳng hóa dữ liệu JSON thành bảng
        df = pd.json_normalize(data)

        # 3. Sử dụng XlsxWriter với cấu hình KHÔNG tự chuyển đổi chuỗi thành công thức
        writer = pd.ExcelWriter(output_path, engine='xlsxwriter', engine_kwargs={'options': {'strings_to_formulas': False}})
        
        # 4. Ghi dữ liệu ra Excel
        df.to_excel(writer, index=False, sheet_name='Data_Toan')
        
        # Tăng độ rộng cột để dễ nhìn công thức dài
        worksheet = writer.sheets['Data_Toan']
        worksheet.set_column(0, df.shape[1] - 1, 30)

        writer.close()
        print(f"✅ Đã chuyển đổi nguyên bản thành công!")
        print(f"📍 File lưu tại: {output_path}")

    except Exception as e:
        print(f"❌ Lỗi: {e}")

# --- ĐƯỜNG DẪN FILE CỦA BẠN ---
file_in = r'C:\Users\TL\Desktop\THUCTAP\OCR\Truc\combined_all_renumbered.json'
file_out = r'C:\Users\TL\Desktop\THUCTAP\OCR\Truc\ket_qua_nguyen_ban.xlsx'

json_to_excel_raw(file_in, file_out)