# Audio to Text - Local Whisper

## Chạy lần đầu

1. Cài Python 3 trên Windows.
2. Mở `start.bat`.
3. Chờ pip cài Flask và faster-whisper.
4. Lần chạy đầu tiên, Whisper sẽ tải model `small`.
5. Mở Chrome và vào:
   http://127.0.0.1:5000

## Sử dụng

- Kéo MP3/WAV/M4A... vào trang.
- Chọn ngôn ngữ hoặc để tự nhận diện.
- Bấm "Chuyển sang văn bản".
- Copy hoặc tải TXT.

## Model

Mặc định: `small`, chạy CPU với int8.

Trong `app.py`:
    MODEL_SIZE = "small"

Có thể đổi:
- `base`: nhanh hơn, độ chính xác thấp hơn.
- `small`: cân bằng.
- `medium`: chính xác hơn nhưng nặng/chậm hơn.

Lưu ý: lần đầu cần Internet để tải model. Sau khi model đã được tải và lưu vào cache, Whisper có thể chạy local mà không cần gửi audio lên API.
