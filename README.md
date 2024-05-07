## Flask CV Processor API

This is a Flask API application for processing CV files. It allows users to upload CV files and retrieve important information from those files in JSON format.

## Features

Users can send POST requests to upload CV files. The CV files can have extensions such as .txt, .doc, .docx, .pdf.
After the CV file is uploaded, the API uses a processor to process the content of the CV file and extract important information from it. The API returns important information from the CV files in JSON format.

## Usage (Installing and running on Ubuntu Server)

This Flask API application processes CV files, extracting important information and returning it in JSON format. It's powered by Gunicorn, a Python WSGI HTTP server.

1. Open a terminal.
2. You can generate self-signed certificates easily from the command line. All you need is to have openssl installed:

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

This command writes a new certificate in cert.pem with its corresponding private key in key.pem, with a validity period of 365 days.

3. Navigate to the directory containing cv_extraction_service.sh. 4. Run the following command to execute cv_extraction_service.sh:

```bash
./cv_extraction_service.sh
```

Note:
Before running the above command, you may need to grant execute permission to cv_extraction_service.sh using the `chmod +x cv_extraction_service.sh` command.

5. After running cv_extraction_service.sh, the server will be started on port 1300 with the endpoint http://localhost:1300/extract-cv.

6. To check status or stop the service, you can use the `sudo systemctl stop` command:

Check status the service

```bash
sudo systemctl status your_service.service
```

Stop the service

```bash
sudo systemctl stop your_service.service
```
