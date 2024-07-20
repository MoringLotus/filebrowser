import requests
import json

def createFile(access_token, drive_id, parent_file_id, name, file_type, check_name_mode='auto_rename'):
    """
    创建文件或文件夹
    
    :param access_token: 访问令牌
    :param drive_id: 驱动器 ID
    :param parent_file_id: 父目录 ID，上传到根目录时填写 'root'
    :param name: 文件或文件夹名称
    :param file_type: 类型，'file' 或 'folder'
    :param check_name_mode: 命名冲突处理模式，'auto_rename' 自动重命名，'refuse' 同名不创建，'ignore' 同名文件可创建
    :return: 创建结果
    """
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/create"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "drive_id": drive_id,
        "parent_file_id": parent_file_id,
        "name": name,
        "type": file_type,
        "check_name_mode": check_name_mode
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        creation_result = response.json()
        return creation_result
    else:
        print(f"Failed to create file, status code: {response.status_code}")
        print("Response text:", response.text)
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_id = "53794254"
parent_file_id = "root"  # 例如上传到根目录
name = "local.txt"
file_type = "file"  # 或者 "folder" 来创建文件夹
check_name_mode = "auto_rename"  # 命名冲突处理模式

creation_result = create_file(access_token, drive_id, parent_file_id, name, file_type, check_name_mode)
if creation_result:
    print("File Creation Result:", creation_result)
    print("File ID:", creation_result.get("file_id"))