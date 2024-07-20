import requests
import json

def get_drive_info(access_token):
    """
    获取用户的 drive 信息
    
    :param access_token: 访问令牌
    :return: 用户的 drive 信息
    """
    url = "https://openapi.alipan.com/adrive/v1.0/user/getDriveInfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        drive_info = response.json()
        return drive_info
    else:
        print(f"Failed to get drive info, status code: {response.status_code}")
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_info = get_drive_info(access_token)
if drive_info:
    print("Drive Info:", drive_info)
    # 打印一些关键信息
    print("User ID:", drive_info.get("user_id"))
    print("Name:", drive_info.get("name"))
    print("Avatar:", drive_info.get("avatar"))
    print("Default Drive ID:", drive_info.get("default_drive_id"))
    if "resource_drive_id" in drive_info:
        print("Resource Drive ID:", drive_info.get("resource_drive_id"))
    if "backup_drive_id" in drive_info:
        print("Backup Drive ID:", drive_info.get("backup_drive_id"))