from flask import Flask, render_template, request, jsonify
from faster_whisper import WhisperModel
from pathlib import Path
import uuid

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024  # 1 GB

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# "small" is a good starting point for a CPU-only PC.
# You can change this to "base" for faster processing or "medium" for better accuracy.
MODEL_SIZE = "small"

print(f"Loading Whisper model: {MODEL_SIZE}")
model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)
print("Whisper is ready.")

ALLOWED_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".mp4", ".webm",
    ".ogg", ".flac", ".aac", ".wma"
}

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe():
    file = request.files.get("audio")
    language = request.form.get("language", "auto")

    if not file or not file.filename:
        return jsonify({"error": "Bạn chưa chọn file âm thanh."}), 400

    ext = Path(file.filename).suffix.lower()

    if ext not in ALLOWED_EXTENSIONS:
        return jsonify({
            "error": "Định dạng chưa được hỗ trợ. Hãy dùng MP3, WAV, M4A, MP4, WEBM, OGG, FLAC, AAC hoặc WMA."
        }), 400

    temp_name = f"{uuid.uuid4().hex}{ext}"
    temp_path = UPLOAD_DIR / temp_name

    try:
        file.save(temp_path)

        selected_language = None if language == "auto" else language

        segments, info = model.transcribe(
            str(temp_path),
            language=selected_language,
            beam_size=5,
            vad_filter=True
        )

        text_parts = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                text_parts.append(text)

        transcript = " ".join(text_parts).strip()

        return jsonify({
            "success": True,
            "text": transcript,
            "language": info.language,
            "language_probability": round(info.language_probability, 3)
        })

    except Exception as e:
        return jsonify({
            "error": f"Không thể chuyển đổi file: {str(e)}"
        }), 500

    finally:
        try:
            temp_path.unlink(missing_ok=True)
        except Exception:
            pass


@app.errorhandler(413)
def too_large(_):
    return jsonify({"error": "File quá lớn. Kích thước tối đa là 1 GB."}), 413


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
