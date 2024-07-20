import requests
import json
def get_upload_url(access_token, drive_id, file_id, upload_id, part_info_list):
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/getUploadUrl"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    body = {
        "drive_id": drive_id,
        "file_id": file_id,
        "upload_id": upload_id,
        "part_info_list": part_info_list
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        upload_info = response.json()
        return upload_info
    else:
        print(f"Failed to get upload URL, status code: {response.status_code}")
        return None

# 使用示例
access_token = "your_access_token_here"
drive_id = "your_drive_id_here"
file_id = "your_file_id_here"
upload_id = "your_upload_id_here"
part_info_list = [
    {"part_number": 1},
    {"part_number": 2}
]

upload_info = get_upload_url(access_token, drive_id, file_id, upload_id, part_info_list)
if upload_info:
    print("Upload Info:", json.dumps(upload_info, indent=4))