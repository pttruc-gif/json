import re
from pathlib import Path

# ======================
# CONFIG
# ======================
INPUT_MD = "/home/npquy/DeepSeek-OCR/DeepSeek_OCR-master/Truc/markdown/v.md"
OUTPUT_MD = "dav.md"

def final_clean_split():
    # 1. ĐỌC FILE
    text = Path(INPUT_MD).read_text(encoding="utf-8")

    # 2. BƯỚC LÀM SẠCH ĐẶC BIỆT (ANTI-PAGE NUMBERS)
    # Xóa các dòng chỉ chứa duy nhất một con số (thường là số trang OCR quét được)
    # Regex nàcdy tìm: Bắt đầu dòng -> có thể có khoảng trắng -> 1 hoặc vài chữ số -> hết dòng
    text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

    # Xóa các ký tự rác hoặc dấu > còn sót
    text = re.sub(r'^\s*>\s*', '', text, flags=re.MULTILINE)

    # 3. CHUẨN HÓA CÂU (NHẬN DIỆN CÂU CÓ NỘI DUNG)
    # Chúng ta chỉ coi là Câu mới nếu: Số thứ tự + có chữ đi kèm phía sau
    # Regex này yêu cầu sau số thứ tự phải có ít nhất vài chữ cái (văn bản)
    pattern_cau = r'(?m)^\d+\.'
    text = re.sub(pattern_cau, r'\n\n\g<0>', text)


    # Chuẩn hóa từ khóa GIẢI
    text = re.sub(
    r'\n\s*(?:###|##|\*\*)?\s*(?:Giải|Lời giải|Hướng dẫn giải)[:.]?\s*(?:\*\*)?\s*\n?', 
    r'\n\nGIẢI_TOKEN\n\n', 
    text, 
    flags=re.IGNORECASE
)

    # 4. TÁCH KHỐI
    blocks = re.split(pattern_cau, text)

    final_output = []

    for block in blocks:
        block = block.strip()
        if not block: continue
        
        # 5. TÁCH ĐỀ VÀ GIẢI
        if 'GIẢI_TOKEN' in block:
            parts = block.split('GIẢI_TOKEN', 1)
            de_bai = parts[0].strip()
            loi_giai = parts[1].strip()
        else:
            # Dự phòng khi không có chữ "Giải"
            sub_parts = re.split(r'\n(?=\$\$|Ta có|Khi đó|Chứng minh|Xét)', block, maxsplit=1)
            if len(sub_parts) == 2:
                de_bai = sub_parts[0].strip()
                loi_giai = sub_parts[1].strip()
            else:
                de_bai = block
                loi_giai = "*(Chưa tách được lời giải)*"

        # 6. FORMAT ĐẦU RA
        de_bai_clean = re.sub(r'^(###|##|\*\*)\s*', '', de_bai).replace('**', '')
        
        entry = f"### BÀI TOÁN: {de_bai_clean}\n\n"
        entry += f"**[LỜI GIẢI CHI TIẾT]**\n\n{loi_giai}\n\n"
        entry += "\n\n---\n\n" # Dấu gạch ngang để báo hiệu HẾT 1 BÀI
        final_output.append(entry)

    # 7. XUẤT FILE
    output_text = "\n\n\n".join(final_output)
    Path(OUTPUT_MD).write_text(output_text, encoding="utf-8")
    print(f"✅ Đã xử lý xong! Đã loại bỏ số trang và tách thành {len(final_output)} bài.")

if __name__ == "__main__":
    final_clean_split()