from abc import abstractmethod
from dataclasses import dataclass
from tqdm import tqdm
import io
import os
import json
from ali.Scaffolding import *
from ali.config.aliConfig import *
import requests
import base64
from pathlib import Path
from typing import Union
from starlette.responses import StreamingResponse
from fastapi import FastAPI
import re
import hashlib
import subprocess
app = FastAPI()

backend_mapping = {}
def file_backend(backend_class):
    """decorator to register a file backend class"""
    backend_mapping[backend_class.__name__] = backend_class
    return backend_class


class File:
    def __init__(self, path: str):
        self.path = path  
    
    def getAccessToken(self):
        pass
    
    @staticmethod
    def parse(file_str):
        mapping = {
            "local": LocalInterface,
            "http": HTTPFile,
        }
        backend, path = file_str.split("://", 1)
        klass = mapping[backend]
        return klass(path)

    @abstractmethod
    def diskLogin(self):
        raise NotImplementedError()
    
    @abstractmethod
    def write(self, bytes: bytes) -> None:
        """创建并写入一个文件"""
        raise NotImplementedError

    def get_media_type(self) -> str:
        """通过文件名获取文件的MIME类型"""
        ext_name = self.path.split(".")[-1]
        ext_mapping = {
            "txt": "text/plain",
            "jpg": "image/jpeg",
            "png": "image/png",
            "pdf": "application/pdf",
        }
        return ext_mapping[ext_name]

    def move(self, dest: str) -> None:
        dest_file = File.parse(dest)
        if dest_file.__class__ != self.__class__:
            dest_file.write(self.read())
            os.remove(self.path)
        else:
            self.same_backend_move(dest_file)



@file_backend
class LocalFile(File):
    
    def same_backend_move(self, dest):
        #os.rename(self.path, dest.path)
        raise NotImplementedError
        pass
    
    # Stream Return 
    def read(self) -> bytes:
        with open(self.path, "rb") as f:
            return f.read()

    # Stream W
    def write(self, bytes) -> None:
        with open(self.path, "wb") as f:
            f.write(bytes)


@file_backend
class HTTPFile(File):

    def read(self) -> bytes:
        resp = requests.get(self.path)
        return resp.content



class AliFile:
    def __init__(self, access_token):
        self.access_token = access_token
        self.drive_id = self.getDriveId()
    """
        *** 初始化时会调用，获取DriveID
    """
    def getDriveId(self):
        headers = {
        "Authorization": f"Bearer {self.access_token}",
        }
        response = requests.post(HOST_NAME + ADRIVE_USER_GETDRIVE_INFO
                                 , headers=headers)
        if response.status_code == 200:
            drive_info = response.json()
            return drive_info.get("default_drive_id")
        else:
            print(f"Failed to get drive info, status code: {response.status_code}")
            return None
    """
        *** 获取文件列表（非递归）
    """
    def getFileList(self,target_dir_id):
        """
            target_dir_id: 根目录可以直接填写root， 递归调用可以参考RecursionGetFileList 
            获取文件列表
            :param access_token: 访问令牌_id
            :param drive_id: 驱动器 ID
            :param limit: 返回的文件列表数量限制，默认为 10
            :return: 文件列表
        """
        headers = {
        "Authorization": f"Bearer {self.access_token}",
        "Content-Type": "application/json"
        }
        body = {
        "drive_id": self.drive_id,
        "parent_file_id": target_dir_id
        }
        response = requests.post(
            HOST_NAME + ADRIVE_OPENFILE_LIST, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            file_list = response.json()
            return file_list
        else:
            print(f"Failed to get file list, status code: {response.status_code}")
            print("Response text:", response.text)  # 打印响应文本
            return None
    """
        *** 获取文件列表（非递归）
    """
    def recursionGetFileList(self, input_path):
        parts = self.splitPath(input_path)
        folder_id = "root"
        for part in parts:
            # 如果不是file_name（xx.xxxx）形式 继续
            if re.match(r'^(.*?)(\.[^.]+)$', part):
                continue
            else:
                # 文件路径要从root开始， 所以先从root下找到part的file_id
                try:
                # file_list 是dict 组成 的 list
                    file_list = self.getFileList(folder_id)["items"]
                    folder_id = next( (i['file_id'] for i in file_list if i["name"] == part), None)
                    print(folder_id)
                except ValueError :
                    print("Invalid path name, please recheck!")      
        file_list = self.getFileList(folder_id)["items"]
        folder_id = next( (i['file_id'] for i in file_list if i["name"] == part), None)    
        return file_list
    """
        *** 获取文件夹ID
    """
    def getSpecificFolderId(self, input_path):
        # 此处的path是 从 root（不用添加root）开始的全路径
        parts = self.splitPath(input_path)
        folder_id = "root"
        # 双向队列
        for part in parts:
            # 如果是file_name（xx.xxxx）形式 继续
            if re.match(r'^(.*?)(\.[^.]+)$', part):
                continue
            else:
                # 文件路径要从root开始， 所以先从root下找到part的file_id
                try:
                # file_list 是dict 组成 的 list
                    file_list = self.getFileList(folder_id)["items"]
                    folder_id = next( (i['file_id'] for i in file_list if i["name"] == part), None)
                    print(folder_id)
                except ValueError :
                    print("Invalid path name, please recheck!")
        return folder_id
    """
        *** 分割： 分割结果带有 / 
        input: /Doc1/Doc2/Doc3
        output_list: ['/Doc1', '/Doc2', '/Doc3']
    """
    def splitPathWithSlash(self, path):
        parts = path.split('/')
    # 移除空字符串部分，例如在路径开头的 '/'
        parts = [part for part in parts if part]
    # 确保每个部分（除了最后一个）都以 '/' 结尾
        path_parts = [f"/{part}" if i < len(parts) - 1 else part for i, part in enumerate(parts)]
        return path_parts
    """
        *** 分割： 分割结果带有 / 
        input: /Doc1/Doc2/Doc3
        output_list: ['Doc1', 'Doc2', 'Doc3']
    """
    def splitPath(self, path):
        parts = [part for part in path.split('/') if part]
        return parts

    """
    Root目录下的文件直接写文件名
    Root目录下的文件夹里的文件"/root目录文件夹/文件夹内文件
    """
    def getFileInfoByPath(self, file_path):
        """
        根据文件路径查找文件
        :param access_token: 访问令牌
        :param drive_id: 驱动器 ID
        :param file_path: 文件路径
        :return: 文件详情
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "drive_id": self.drive_id,
            "file_path": file_path
        }
        response = requests.post(HOST_NAME + ADRIVE_OPENFILE_GET_BY_PATH, headers=headers, json=body)
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
            # print("File ID:", file_details.get("file_id"))
            # print("Name:", file_details.get("name"))
            # print("Type:", file_details.get("type"))
            # print("Size:", file_details.get("size"))
            # print("Created At:", file_details.get("created_at"))
            # print("Updated At:", file_details.get("updated_at"))
            return file_details
        else:
            print(f"Failed to get file by path, status code: {response.status_code}")
            print("Response text:", response.text)
            return None

    """
        *** 获取下载链接： 通过file_id
    """
    def getFileDownloadUrl(self, file_id):
        """
        获取文件详情
        :param access_token: 访问令牌
        :param drive_id: 驱动器 ID
        :param file_id: 文件 ID
        :return: 文件详情
        """
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "drive_id": self.drive_id,
            "file_id": file_id
        }
        response = requests.post(HOST_NAME + ADRIVE_OPENFILE_GET_DOWNLOAD_URL 
                                 , headers=headers, json=body)
        if response.status_code == 200:
            file_details = response.json()
            return file_details['url']
        else:
            print(f"Failed to get file details, status code: {response.status_code}")
            print("Response text:", response.text)
            return None
        """
            根据获取到的URL下载，返回进度 186MiB [06:13, 498kiB/s]
        """
    
    
    """
        分片可能有多个
        ***创建文件： 上传（此处指上传一个分片）的第一步，返回    
            file_id = file_info["file_id"]
            upload_id = file_info["upload_id"]
            part_info_list = file_info["part_info_list"]
    """
    def createFile(self, parent_file_id, name, file_type, check_name_mode):
        url = "https://openapi.alipan.com/adrive/v1.0/openFile/create"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "drive_id": self.drive_id,
            "parent_file_id": parent_file_id,
            "name": name,
            "type": file_type,
            "check_name_mode": check_name_mode
        }
        
        response = requests.post(HOST_NAME + ADRIVE_OPENFILE_CREATE
                                 , headers=headers, json=body)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to create file, status code: {response.status_code}, response: {response.text}")
            return None
    """
        ***创建传递大文件的函数
    """
    def createFile(self, parent_file_id, name, file_type, check_name_mode):
        pass
    """
        ***获取上传链接:
            上传文件的第二部：通过创建文件得到的信息来获取链接
            upload_info = get_upload_url(access_token, drive_id, file_id, upload_id,part_info_list)
            upload_url = upload_info["part_info_list"][0]["upload_url"]
            
    """
    def getUploadUrl(self, file_id, upload_id, part_info_list):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "drive_id": self.drive_id,
            "file_id": file_id,
            "upload_id": upload_id,
            "part_info_list": part_info_list
        }
        response = requests.post(HOST_NAME + ADRIVE_OPENFILE_GET_UPLOAD_URL
                                 , headers=headers, json=body)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to get upload URL, status code: {response.status_code}, response: {response.text}")
            return None
    
    """ 
        ***上传文件：
            通过前一步得到的upload_url实现上传操作
    """
    def uploadFile(self, file_path, upload_url):
        with open(file_path, 'rb') as file:
            #response = requests.put(upload_url, headers=headers, data=file.read())
            response = requests.put(url = upload_url, data=file.read())
        if response.status_code == 200:
            return {"part_number": 1, "etag": response.headers.get("ETag")}
        else:
            print(f"Failed to upload file, status code: {response.status_code}, response: {response.text}")
            return None
    """
        ***上传的最后一步操作:
        结束上传
    """
    def completeUpload(self, file_id, upload_id, file_name, file_size, content_hash):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "drive_id": self.drive_id,
            "file_id": file_id,
            "upload_id": upload_id,
            "name": file_name,
            "size": file_size,
            "content_hash": content_hash
        }
        
        response = requests.post(HOST_NAME + ADRIVE_OPENFILE_COMPLETE
                                 , headers=headers, json=body)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to complete upload, status code: {response.status_code}, response: {response.text}")
            return None
    
    """
        ***上传直接调用： 该函数只能上传大小小于5个G的
                check_name_model : auto_rename 自动重命名，存在并发问题 |
                                   refuse      同名不创建              |
                                   ignore       同名文件可创建
                file_type        : file | folder
                local_path       : "/home/featurize/work/filebrowser/filebrowser/ali/Scaffolding/createAndDownload/ExampleFile.txt"
                                   
    """
    
    ### ???? 杂糅
    def getFileUploadWithPath(self, local_path, parent_file, name, file_type, check_name_mode):
        parent_file_id = self.getSpecificFolderId(parent_file)
        file_info = self.createFile(parent_file_id, name, file_type, check_name_mode)
        if file_info and file_info.get("file_id") and file_info.get("upload_id"):
            file_id = file_info["file_id"]
            upload_id = file_info["upload_id"]
            part_info_list = file_info["part_info_list"]
            # 获取上传URL
            upload_info = ali.getUploadUrl(file_id, upload_id,part_info_list)
            if upload_info and upload_info.get("part_info_list"):
                # upload_info 格式? 获取 part_info_list 大小
                upload_url = upload_info["part_info_list"][0]["upload_url"]
                file_path = local_path
                #file_path = "/home/featurize/work/filebrowser/filebrowser/ali/Scaffolding/createAndDownload/ExampleFile.txt"
                # 获取文件大小
                file_size = os.path.getsize(file_path)
                # 上传文件
                part = ali.uploadFile(file_path, upload_url)
                if part:
                    # 生成秒传校验码
                    content_hash = ali.generateProofCode(file_path, file_size)
                    # 标记文件上传完毕
                    complete_info = ali.completeUpload(file_id, upload_id, name, file_size, content_hash)
                    if complete_info:
                        print("Upload completed:", json.dumps(complete_info, indent=4))
                    else:
                        print("Failed to complete upload.")
                else:
                    print("Failed to upload file.")
            else:
                print("Failed to get upload URL.")
        else:
            print("Failed to create file.")
    
    def getBigFile
        
    def generateProofCode(self, file_path, file_size):
        proof_range = self.getProofRange(file_size)
        with open(file_path, 'rb') as file:
            file.seek(proof_range["Start"])
            file_data = file.read(proof_range["End"] - proof_range["Start"])
        return base64.b64encode(file_data).decode('utf-8')

    def getProofRange(self, file_size):
        if file_size == 0:
            return {"Start": 0, "End": 0}
        access_token_md5 = hashlib.md5(self.access_token.encode('utf-8')).hexdigest()[:16]
        token_int = int(access_token_md5, 16)
        index = token_int % file_size
        proof_range = {"Start": index, "End": min(index + 8, file_size)}
        return proof_range
    
    def downloadFile(self, url, file_path):
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size_in_bytes = int(r.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(file_path, 'wb') as file:
                for data in r.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")
                
    def getFileDownloadByPath(self, file_path, target_path):
        file_id = self.getFileInfoByPath(file_path).get("file_id")
        file_download_url = self.getFileDownloadUrl(file_id)
        self.downloadFile(file_download_url, target_path)
        
    def searchFiles(self, query, limit=10):
        """
        在指定的 drive_id 中搜索文件
        :param access_token: 访问令牌
        :param drive_id: 驱动器 ID
        :param query: 搜索关键词
        :param limit: 返回的文件列表数量限制，默认为 10
        :return: 搜索结果或错误信息
        """
        
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
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "drive_id": self.drive_id,
            "query": query,
            "limit": limit
        }
        response = requests.post(HOST_NAME + ADRIVE_OPENFILE_SEARCH, 
                                 headers=headers, 
                                 json=body)
        if response.status_code == 200:
            search_result = response.json()
            return search_result
        else:
            print(f"Failed to search files, status code: {response.status_code}")
            print("Response text:", response.text)  # 打印响应文本
            return None
@dataclass
class FileStat:
    name: str
    size: int
    mtime: int
    is_dir: bool


@app.get("/files/list")
def get_list(path: str):
    path = Path(path)
    print(path)
    return [
        FileStat(f.name, f.stat().st_size, f.stat().st_mtime, f.is_dir())
        for f in path.iterdir()
    ]


@app.post("/files/move")
def get_list(src: str, dest: str):
    src = File.parse(src)
    src.move(dest)
    return {"message": "File moved successfully"}


@app.post("/files/copy")
def copy_file(src: str, dest: str):
    src = File.parse(src)
    dest = File.parse(dest)
    dest.write(src.read())
    return {"message": "File copied successfully"}


@app.post("/files")
def create_file(path: str, content: str):
    """Upload file to path"""
    #file = File.parse()
    pass


@app.get("/files/get_file")
def get_file(path: str):
    """Download file"""
    # 获取类
    file = File.parse(path)
    # 调用类中read方法
    bytes = file.read()
    media_type = file.get_media_type()
    return StreamingResponse(io.BytesIO(bytes), media_type=media_type)

if __name__ == "__main__":
    access_token = "eyJraWQiOiJLcU8iLCJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsImF1ZCI6ImRkOGQ5MmZlMWY2NTRkNzk4OWMwNWUwNDU0NWZhMzI0IiwicyI6ImNkYSIsImQiOiIzMTg5OTY2MTQwLDUzNzk0MjU0IiwiaXNzIjoiYWxpcGFuIiwiZXhwIjoxNzIzNzk5NjI4LCJpYXQiOjE3MjEyMDc2MjUsImp0aSI6ImUyNjFiZGYzZGNhMTRhOWFhNDk1MmZhYTUyMjE0OTdiIn0.ZC1Ue-toKlLIU-FJUJX3VTAWwbAOBa4w-GVyHElegj4"
    ali = AliFile(access_token)
    name = "logo.txt"
    file_info = ali.createFile(parent_file_id = "root", name = "logo.txt", file_type = "file", check_name_mode = "auto_rename")
    print(file_info)
    if file_info and file_info.get("file_id") and file_info.get("upload_id"):
        file_id = file_info["file_id"]
        upload_id = file_info["upload_id"]
        part_info_list = file_info["part_info_list"]
        # 获取上传URL
        upload_info = ali.getUploadUrl(file_id, upload_id,part_info_list)
        if upload_info and upload_info.get("part_info_list"):
            upload_url = upload_info["part_info_list"][0]["upload_url"]
            file_path = "/home/featurize/work/filebrowser/filebrowser/ali/Scaffolding/createAndDownload/ExampleFile.txt"
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            # 上传文件
            part = ali.uploadFile(file_path, upload_url)
            if part:
                # 生成秒传校验码
                content_hash = ali.generateProofCode(file_path, file_size)
                # 标记文件上传完毕
                complete_info = ali.completeUpload(file_id, upload_id, name, file_size, content_hash)
                if complete_info:
                    print("Upload completed:", json.dumps(complete_info, indent=4))
                else:
                    print("Failed to complete upload.")
            else:
                print("Failed to upload file.")
        else:
            print("Failed to get upload URL.")
    else:
        print("Failed to create file.")