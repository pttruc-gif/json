import pandas as pd

def export_long_content(file_path, threshold=2000):
    df = pd.read_excel(file_path).fillna("")
    
    # Tính độ dài
    df['problem_len'] = df['problem'].astype(str).apply(len)
    df['answer_len'] = df['answer'].astype(str).apply(len)
    
    # Lọc câu dài
    long_rows = df[(df['problem_len'] > threshold) | (df['answer_len'] > threshold)]
    
    if long_rows.empty:
        print("Không có câu nào dài vượt ngưỡng.")
        return

    # 1. Xuất ra EXCEL (Để quản lý)
    long_rows.to_excel("danh_sach_cau_dai.xlsx", index=False)
    
    # 2. Xuất ra TXT (Để đọc soát lỗi LaTeX)
    with open("danh_sach_cau_dai.txt", "w", encoding="utf-8") as f:
        for _, row in long_rows.iterrows():
            f.write(f"--- ID: {row['id']} ---\n")
            f.write(f"[ĐỘ DÀI PROBLEM: {row['problem_len']}]\n{row['problem']}\n\n")
            f.write(f"[ĐỘ DÀI ANSWER: {row['answer_len']}]\n{row['answer']}\n")
            f.write("-" * 80 + "\n\n")

    print(f"Đã xuất xong {len(long_rows)} câu dài ra cả 2 file .xlsx và .txt")

# Chạy lệnh
export_long_content(r'C:\Users\TL\Desktop\THUCTAP\OCR\Truc\ket_qua_nguyen_ban.xlsx')