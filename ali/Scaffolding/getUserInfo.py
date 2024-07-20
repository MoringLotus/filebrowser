import requests

def get_user_info(access_token):
    url = "https://openapi.alipan.com/oauth/users/info"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        print(f"Failed to get user info, status code: {response.status_code}")
        return None

# 使用示例
access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
user_info = get_user_info(access_token)
if user_info:
    print("User Info:", user_info)