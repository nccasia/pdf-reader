import os
from flask import Flask, request, jsonify
from processor.gemini_processor import GeminiProcessor
import io
from flask_cors import CORS

ALLOWED_EXTENSIONS = {"txt", "doc", "docx", "pdf"}

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv("CORS_ORIGIN")}})
processor = GeminiProcessor()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/extract-cv", methods=["GET"])
def get_extract_cv():
    return jsonify({"Message": "This is a GET request to /extract-cv"}), 200


@app.route("/extract-cv", methods=["POST"])
def extract_cv():
    if "file" not in request.files:
        return (
            jsonify({"Error": "No file part"}),
            400,
        )
    file = request.files["file"]
    if file.filename == "":
        return (
            jsonify({"Error": "No selected file"}),
            400,
        )
    if not allowed_file(file.filename):
        return (
            jsonify(
                {
                    "Error": "Invalid file extension. Supported file extensions are .txt, .doc, .docx, .pdf"
                }
            ),
            400,
        )
    try:
        attachment_data = processor.process(
            io.BytesIO(file.read()), os.path.splitext(file.filename)[1]
        )
        response = processor.get_response(attachment_data)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT"))
