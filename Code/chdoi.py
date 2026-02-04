import re
import json
from pathlib import Path

# ======================
# CONFIG
# ======================
INPUT_MD = "/home/npquy/DeepSeek-OCR/DeepSeek_OCR-master/Truc/markdown/Ebook cơ sở lý thuyết và một số bài toán về dãy số.md"      # File Markdown của bạn
OUTPUT_JSON = "ebook.json"  # File JSON kết quả

def convert_md_to_json_multi_tokens():
    # 1. Đọc file
    if not Path(INPUT_MD).exists():
        print(f"Lỗi: Không tìm thấy file {INPUT_MD}")
        return
    
    content = Path(INPUT_MD).read_text(encoding="utf-8")

    # 2. TÁCH BÀI: Dựa vào khoảng trống 3 dòng (\n\n\n) hoặc nhiều hơn
    # Regex \n{3,} tìm các đoạn ngắt quãng lớn giữa các bài
    blocks = re.split(r'\n{3,}', content)

    json_data = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # 3. CHIA ĐỀ VÀ GIẢI: Nhận diện đồng thời 3 loại Token
        # Regex tìm: GIẢI_TOKEN HOẶC **[LỜI GIẢI CHI TIẾT]** HOẶC ## Giải
        # Dấu \*\* dùng để thoát ký tự đặc biệt của Markdown
        split_pattern = r'\n\s*(?:GIẢI_TOKEN|\*\*\[LỜI GIẢI CHI TIẾT\]\*\*|## Giải|##Giai)\s*\n'
        
        parts = re.split(split_pattern, block, maxsplit=1, flags=re.IGNORECASE)

        if len(parts) >= 2:
            # Tách thành công Đề và Giải
            problem_text = parts[0].strip()
            answer_text = parts[1].strip()
            
            # Làm sạch các Header bài toán cũ nếu có
            problem_text = re.sub(r'^(### BÀI TOÁN:|###|##)\s*', '', problem_text).strip()
            
            # Làm sạch các dấu kẻ ngang --- còn sót lại cuối lời giải
            answer_text = re.sub(r'\n\s*-{3,}\s*$', '', answer_text).strip()

            json_data.append({
                "problem": problem_text,
                "answer": answer_text
            })
        else:
            # Nếu không tìm thấy các Token ngăn cách
            problem_text = re.sub(r'^(### BÀI TOÁN:|###|##)\s*', '', block).strip()
            json_data.append({
                "problem": problem_text,
                "answer": "*(Không tìm thấy dấu mốc lời giải)*"
            })

    # 4. XUẤT FILE JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Đã chuyển đổi {len(json_data)} bài tập sang JSON.")
    print(f"📍 Kết quả lưu tại: {OUTPUT_JSON}")

if __name__ == "__main__":
    convert_md_to_json_multi_tokens()