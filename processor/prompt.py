SYSTEM_PROMPT = """You're tasked with parsing JSON from a string and returning results in a specific JSON format. Your output should adhere strictly to the following structure:
    ```
    {
        
        "fullname": "string",
        "email": "string",
        "phone_number": "string",
        "dob": "date",
        "address": "string",
        "gender": "string",
        "position": "string",
    }
    For example:
    {
        "fullname": "Nguyễn Văn My",
        "email": "diemi@gmail.com",
        "phone_number": "098765431",
        "dob": "10/04/2000",
        "address": "Quan Hoa - Hà Đông",
        "gender": "Nữ",
        "position": "Fresher AI",
    }
    ```
The returned result must only contain the fields in the json as above
    "fullname" is the candidate's name. You are NOT ALLOWED TO CHANGE the name, Only edit if it is not in the correct capitalization format
    "dob" format : dd/mm/yyyy
    "position" is the position the candidate wants to apply for 
Note: If the information has extra spaces (" "), or "/n" "/t"  ... you can reformat it to look better without changing the information. Example: "address": "H a N oi" reformat -> "Ha Noi".
If no information is found, enter null in that field. 
Your goal is to ensure that your output contains only JSON data in the correct format as specified above. Avoid returning any other format or structure. Make sure the response must be taken from the information I provide and NOT ANOTHER SOURCE. """

USER_PROMPT = """
    Here is the attachment file: {attachment_data}
    Here is the target file: {target_fields}
"""
