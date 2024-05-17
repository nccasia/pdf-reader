import os
from flask import Flask, request, jsonify, Response
from processor.gemini_processor import GeminiProcessor
import io
import requests
import fitz
from flask_cors import CORS

ALLOWED_EXTENSIONS = {"doc", "docx", "pdf"}

cors_origin = os.getenv("CORS_ORIGIN")
CORS_ORIGIN = cors_origin.strip().strip('"')
CORS_ORIGIN_LIST = CORS_ORIGIN.split('", "')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": CORS_ORIGIN_LIST}}, supports_credentials=True)
processor = GeminiProcessor()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/check_connection", methods=["GET"])
def check_connection():
    return Response(status=200)


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
                    "Error": "Invalid file extension. Supported file extensions are .doc, .docx, .pdf"
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


class PDFProcessor:
    @staticmethod
    def extract_text_from_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            pdf_document = fitz.open(stream=io.BytesIO(response.content))
            text = ""
            for page_number, page in enumerate(pdf_document):
                text += page.get_text()

            return text
        else:
            return None


@app.route("/extract-multifile", methods=["POST"])
def extract_multifile():
    data = request.get_json()
    if "urls" not in data:
        return jsonify({"Error": "No URLs provided"}), 400

    urls = data["urls"]

    if len(urls) > 10:
        return jsonify({"Error": "Too many URLs provided. Maximum limit is 10."}), 400
    data_cv = []
    i = 1
    for url in urls:
        data_cv.append(f"\n---------- This is CV {i} ----------\n")
        i += 1
        data_cv.append(PDFProcessor.extract_text_from_url(url))
        data_cv.append("\n")
    text = "".join(data_cv)
    response = processor.get_response_multi(text)
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT"))
