import requests
def getFileDownload(access_token, drive_id, file_id):
    """
    获取文件详情
    :param access_token: 访问令牌
    :param drive_id: 驱动器 ID
    :param file_id: 文件 ID
    :return: 文件详情
    """
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/getDownloadUrl"
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
        return file_details['url']
    else:
        print(f"Failed to get file details, status code: {response.status_code}")
        print("Response text:", response.text)
        return None
    

access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_id = "53794254"
file_id = "66988b83b47a401f944c4397a3a13c110e13bde8"
response =getFileDownload(access_token, drive_id, file_id)
print(response)