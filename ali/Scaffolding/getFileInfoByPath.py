import requests
import json

def get_file_info_by_path(access_token, drive_id, file_path):
    """
    根据文件路径查找文件
    
    :param access_token: 访问令牌
    :param drive_id: 驱动器 ID
    :param file_path: 文件路径
    :return: 文件详情
    """
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/get_by_path"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "drive_id": drive_id,
        "file_path": file_path
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        file_details = response.json()
        """
                print("File ID:", file_details.get("file_id"))
                print("Name:", file_details.get("name"))
                print("Type:", file_details.get("type"))
                print("Size:", file_details.get("size"))
                print("Created At:", file_details.get("created_at"))
                print("Updated At:", file_details.get("updated_at"))
        """
        return file_details
    else:
        print(f"Failed to get file by path, status code: {response.status_code}")
        print("Response text:", response.text)
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_id = "53794254"
file_path = "/Doc1/Doc2"  # 例如查找根目录下的 a.jpeg 文件

file_details = get_file_info_by_path(access_token, drive_id, file_path)
if file_details:
    print("File Details:", file_details)
    # 打印文件详情
    print("File ID:", file_details.get("file_id"))
    print("Name:", file_details.get("name"))
    print("Type:", file_details.get("type"))
    print("Size:", file_details.get("size"))
    print("Created At:", file_details.get("created_at"))
    print("Updated At:", file_details.get("updated_at"))