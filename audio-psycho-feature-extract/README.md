# audio-psycho-feature-extract

Lab tách tin psycho-feature với hai container:

- `sender`: chứa `cover.wav` và `stego.wav` để gửi sang `receiver`
- `receiver`: chứa mã tách tin và file kiểm tra ẩn

Luồng bài lab:

1. Bật SSH trên `sender` và `receiver`
2. Dùng `scp` để gửi `cover.wav` và `stego.wav` sang `receiver`
3. Trên `receiver`, sửa `extract_task.py` để điền tên hai file đầu vào
4. Chạy `python3 extract_task.py` để tạo `recovered.txt`
5. Chạy `cat recovered.txt` để hiện nội dung thông điệp và hoàn tất mục chấm cuối

Checkwork có 3 mục:

- `audio_received`
- `recovered_created`
- `message_recovered`
