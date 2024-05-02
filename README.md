## Flask CV Processor API

This is a Flask API application for processing CV files. It allows users to upload CV files and retrieve important information from those files in JSON format.

## Features

Users can send POST requests to upload CV files. The CV files can have extensions such as .txt, .doc, .docx, .pdf.
After the CV file is uploaded, the API uses a processor to process the content of the CV file and extract important information from it. The API returns important information from the CV files in JSON format.

## Usage

1. Install dependencies

- Using pip

```bash
pip install -r requirements.txt
```

2. Run the code

```bash
python main.py
```
