import pandas as pd
import json
import os

def convert_excel_to_json(file_path, output_name="dataset.json"):
    # 1. Đọc file Excel
    # Nếu file của bạn có nhiều sheet, bạn có thể thêm sheet_name='tên_sheet'
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return

    # 2. Tiền xử lý dữ liệu để làm Dataset LLM
    # Thay thế các giá trị NaN (ô trống) bằng chuỗi rỗng để không làm hỏng JSON
    columns_to_keep = ['id', 'problem', 'answer'] 
# Nếu file của bạn có cột 'result' thì thêm vào: ['id', 'problem', 'answer', 'result']
    df = df[columns_to_keep]
    df = df.fillna("")
    

    # Đảm bảo cột ID là số nguyên (nếu có)
    if 'id' in df.columns:
        df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)

    # 3. Chuyển đổi sang dạng List of Dictionaries
    # orient='records' giữ nguyên các tiêu đề cột của bạn làm Key trong JSON
    data_json = df.to_dict(orient='records')

    # 4. Xuất ra file JSON
    # ensure_ascii=False: Rất quan trọng để giữ nguyên tiếng Việt và các ký hiệu toán học
    # indent=4: Giúp bạn dễ dàng mở file ra kiểm tra bằng mắt thường
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False, indent=4)

    print(f"--- THÀNH CÔNG ---")
    print(f"Đã chuyển đổi {len(data_json)} câu hỏi.")
    print(f"File lưu tại: {os.path.abspath(output_name)}")

# Thay 'ket_qua_nguyen_ban.xlsx' bằng tên file thực tế của bạn
# Sửa dòng 37 thành:
convert_excel_to_json(r'C:\Users\TL\Desktop\THUCTAP\OCR\Truc\ket_qua_nguyen_ban.xlsx')