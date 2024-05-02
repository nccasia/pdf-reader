## Flask CV Processor API

This is a Flask API application for processing CV files. It allows users to upload CV files and retrieve important information from those files in JSON format.

## Features

Users can send POST requests to upload CV files. The CV files can have extensions such as .txt, .doc, .docx, .pdf.
After the CV file is uploaded, the API uses a processor to process the content of the CV file and extract important information from it. The API returns important information from the CV files in JSON format.

## Usage (Installing and running on Ubuntu Server)

1. Open a terminal.
2. Navigate to the directory containing script.sh.
3. Run the following command to execute script.sh:

```bash
./script.sh
```

Note:
Before running the above command, you may need to grant execute permission to script.sh using the `chmod +x script.sh` command.

4. After running script.sh, the server will be started on port 1300 with the endpoint http://localhost:1300/extract-cv.
   If you wish to change the port used by the server, you can do so by modifying the port parameter in the `app.run()` function within the `main.py` file.

5. To stop the service, you can use the `sudo systemctl stop` command:

```bash
sudo systemctl stop your_service.service
```
