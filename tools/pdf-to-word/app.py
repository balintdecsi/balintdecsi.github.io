import os
import tempfile
import uuid

from docx import Document
from docx.shared import Pt
from flask import Flask, render_template, request, send_file

from clean_text import clean_text
from extract_text import extract_text

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 MB

UPLOAD_DIR = os.path.join(tempfile.gettempdir(), "pdf_to_word_uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("pdf")
    if not file or not file.filename.lower().endswith(".pdf"):
        return "Please upload a valid PDF file.", 400

    use_column = request.form.get("column_detection") == "on"

    job_id = uuid.uuid4().hex[:12]
    pdf_path = os.path.join(UPLOAD_DIR, f"{job_id}.pdf")
    docx_path = os.path.join(UPLOAD_DIR, f"{job_id}.docx")

    try:
        file.save(pdf_path)

        raw_text = extract_text(pdf_path, use_column_detection=use_column)
        cleaned = clean_text(raw_text)

        doc = Document()
        style = doc.styles["Normal"]
        style.font.name = "Calibri"
        style.font.size = Pt(12)

        for paragraph in cleaned.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                doc.add_paragraph(paragraph)

        doc.save(docx_path)

        base_name = os.path.splitext(file.filename)[0]
        return send_file(
            docx_path,
            as_attachment=True,
            download_name=f"{base_name}_tts.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    finally:
        for path in (pdf_path, docx_path):
            try:
                os.remove(path)
            except OSError:
                pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
