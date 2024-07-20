import requests
import json

def get_file_details(access_token, drive_id, file_id):
    """
    获取文件详情
    
    :param access_token: 访问令牌
    :param drive_id: 驱动器 ID
    :param file_id: 文件 ID
    :return: 文件详情
    """
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/get"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "drive_id": drive_id,
        "file_id": file_id
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        file_details = response.json()
        return file_details
    else:
        print(f"Failed to get file details, status code: {response.status_code}")
        print("Response text:", response.text)
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_id = "53794254"
file_id = "66976fd454251c84e04143ceb8e67f42e2503deb"

file_details = get_file_details(access_token, drive_id, file_id)
if file_details:
    print("File Details:", file_details)
    # 打印文件详情
    print("File ID:", file_details.get("file_id"))
    print("Name:", file_details.get("name"))
    print("Size:", file_details.get("size"))
    print("Type:", file_details.get("type"))
    print("Created At:", file_details.get("created_at"))
    print("Updated At:", file_details.get("updated_at"))
    if "thumbnail" in file_details:
        print("Thumbnail URL:", file_details.get("thumbnail"))
    if "url" in file_details:
        print("File URL:", file_details.get("url"))