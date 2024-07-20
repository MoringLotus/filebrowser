import requests
import json

import requests

def search_files(access_token, drive_id, query, limit=10):
    """
    在指定的 drive_id 中搜索文件
    
    :param access_token: 访问令牌
    :param drive_id: 驱动器 ID
    :param query: 搜索关键词
    :param limit: 返回的文件列表数量限制，默认为 10
    :return: 搜索结果或错误信息
    """
    url = "https://openapi.alipan.com/adrive/v1.0/openFile/search"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "drive_id": drive_id,
        "query": query,
        "limit": limit
    }
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        search_result = response.json()
        return search_result
    else:
        print(f"Failed to search files, status code: {response.status_code}")
        print("Response text:", response.text)  # 打印响应文本
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
drive_id = "53794254"
"""
查询语句，样例：
        固定目录搜索，只搜索一级 parent_file_id = '123'
        精确查询 name = '123'
        模糊匹配 name match "123"
        搜索指定后缀文件 file_extension = 'apk' 
        范围查询 created_at < "2019-01-14T00:00:00"
        复合查询：
        type = 'folder' or name = '123'
        parent_file_id = 'root' and name = '123' and category = 'video'
"""
query = " name = 'testdoc.txt' "  # 搜索关键词
limit = 20  # 例如限制返回的文件数量为20
search_result = search_files(access_token, drive_id, query, limit)
if search_result:
    print("Search Result:", search_result)
    # 打印文件列表
    files = search_result.get("files", [])
    for file in files:
        print(f"File ID: {file['file_id']}, Name: {file['name']}")