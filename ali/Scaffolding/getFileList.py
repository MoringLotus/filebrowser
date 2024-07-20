import requests
import json

def getFileList(access_token, drive_id, limit=10):
    """
    获取文件列表
    :param access_token: 访问令牌
    :param drive_id: 驱动器 ID
    :param limit: 返回的文件列表数量限制，默认为 10
    :return: 文件列表
    """
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/list"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "drive_id": drive_id,
        "parent_file_id": "root"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(body))
    
    if response.status_code == 200:
        file_list = response.json()
        return file_list
    else:
        print(f"Failed to get file list, status code: {response.status_code}")
        print("Response text:", response.text)
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_id = "53794254"
limit = 20  # 例如获取20个文件

file_list = getFileList(access_token, drive_id, limit)
if file_list:
    print("File List:", file_list["items"])