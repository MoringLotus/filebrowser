import requests
import json
import os
import hashlib
import os
from urllib.parse import quote
from urllib.parse import urlencode
class baidu:
    def __init__(self, app_key, secret_key, sign_key, app_id):
        self.app_key = app_key
        self.secret_key = secret_key
        self.sign_key = sign_key
        self.app_id = app_id
        self.access_token = "121.69ff5daf7caf13080197a32f478fd180.YBLhpiN0ERJaoquTewqT-AxZCR3x-fjGzhSeN8-.a3UOAA"

    def getFileList(self, target_dir):               
        url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=list&dir=/{target_dir}&order=time&start=0&limit=10&web=web&folder=0&access_token={self.access_token}&desc=1"
        payload = {}
        files = {}
        headers = {
        'User-Agent': 'pan.baidu.com'
        }
        response = requests.request("GET", url, headers=headers, data = payload, files = files)

        return json.loads(str(response.text))

    def getFileListRecursion(self, path):
        """
        response = bd.getFileListRecursion("电影")
        print(response)
        """
        url = f"http://pan.baidu.com/rest/2.0/xpan/multimedia?method=listall&path=/{path}&access_token={self.access_token}&web=1&recursion=1&start=0&limit=5"
        payload = {}
        files = {}
        headers = {
        'User-Agent': 'pan.baidu.com'
        }
        response = requests.request("GET", url, headers=headers, data = payload, files = files)
        return json.loads(str(response.text))

    def getFileInfo(self, file_path):
        fs_id = self.getFileIdRecursion(file_path)
        encoded_array = quote(json.dumps(fs_id))
        url = f"http://pan.baidu.com/rest/2.0/xpan/multimedia?method=filemetas&access_token={self.access_token}&fsids={fs_id}&thumb=1&dlink=1&extra=1&detail=1"
        payload = {}
        files = {}
        headers = {
        'User-Agent': 'pan.baidu.com'
        }
        response = requests.request("GET", url, headers=headers, data = payload, files = files)

        return json.loads(str(response.text))

    def getFileIdRecursion(self, file_path):
        directory, filename = os.path.split(file_path)
        url = f"http://pan.baidu.com/rest/2.0/xpan/multimedia?method=listall&path=/{directory}&access_token={self.access_token}&web=1&recursion=1&start=0&limit=5"
        payload = {}
        files = {}
        headers = {
        'User-Agent': 'pan.baidu.com'
        }
        response = requests.request("GET", url, headers=headers, data = payload, files = files)
        response = json.loads(str(response.text))
        result = []
        for i in response['list']:
            if i['server_filename'] == filename:
                result.append(i['fs_id'])
        return result
       
    """
    
    """
    def searchFile(self, name, dir):
        url = f"http://pan.baidu.com/rest/2.0/xpan/file?dir=/{dir}&access_token={self.access_token}&web=1&recursion=1&page=1&num=2&method=search&key={name}"
        payload = {}
        files = {}
        headers = {
            'User-Agent': 'pan.baidu.com'
        }
        response = requests.request("GET", url, headers=headers, data = payload, files = files)
        return json.loads(str(response.text))
    def getDlink(self,file_path):
        response = self.getFileInfo(file_path)
        return response['list'][0]['dlink']
    def getDownload(self, file_path):
        dlink = self.getDlink(file_path)            
        url = f"{dlink}&access_token={self.access_token}"
        payload = {}
        files = {}
        headers = {
        'User-Agent': 'pan.baidu.com'
        }
        response = requests.request("GET", url, headers=headers, data = payload, files = files)
        return response

    def calculate_md5(self, file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def split_file_into_blocks(self, file_path, block_size=4*1024*1024):
        block_list = []
        with open(file_path, "rb") as f:
            while True:
                block = f.read(block_size)
                if not block:
                    break
                block_md5 = hashlib.md5(block).hexdigest()
                block_list.append(block_md5)
        return block_list

    def getblockList(self, file_path):
        file_size = os.path.getsize(file_path)
        if file_size < 4*1024*1024:
            return [calculate_md5(file_path)]
        else:
            return self.split_file_into_blocks(file_path)
    
    def preUpload(self, local_path, target_dir):
        # 分片
        url = f"http://pan.baidu.com/rest/2.0/xpan/file?method=precreate&access_token={self.access_token}"
        block_list = self.getblockList(local_path)
        payload = {'path': f'{target_dir}',
        'size': f'{os.path.getsize(local_path)}',
        'rtype': '1',
        'isdir': '0',
        'autoinit': '1',
        'block_list': f'{json.dumps(block_list)}'}
        print("preUpload:", payload)
        files = {
        }
        headers = {
            "User-Agent": "pan.baidu.com"
        }
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print(json.loads(str(response.text)))
        return json.loads(str(response.text)), block_list
        
    def upload_part(self, part_num, file_content, upload_id, target_path_url_encode):
        """
        上传单个分片。
        :param part_num: 分片序号。
        :param file_content: 分片内容。
        """
        files = {'file': ('part_{}'.format(part_num), file_content)}
        headers = {
        }
        url = f"https://c3.pcs.baidu.com/rest/2.0/pcs/superfile2?method=upload&access_token={self.access_token}&type=tmpfile&path={target_path_url_encode}&uploadid={upload_id}&partseq={part_num}"
        print("URL is :", url)
        response = requests.post(url, headers=headers, files=files)
        print(response.text)
        return response.ok
    # 分片上传
    def getSplitUpload(self, preupload_result,file_path, target_path_url_encode): 
        upload_id = preupload_result.get('uploadid')
        block_list = preupload_result.get('block_list')  # 分片序号列表
        file_size = os.path.getsize(file_path)
        part_size = 4 * 1024 * 1024  # 4MB
        headers = {
        'Content-Type': 'multipart/form-data'
        }
        with open(file_path, 'rb') as f:
            for part_num in block_list:  # 使用索引遍历分片
                part_start = part_num * part_size  # 分片的起始字节位置
                part_end = min((part_num + 1) * part_size, file_size)  # 分片的结束字节位置，最后一个分片可能小于part_size
                # 定位到分片的起始位置
                f.seek(part_start)
                # 读取分片数据
                part_data = f.read(part_end - part_start)
                # 调用 upload_part 函数上传分片
                success = self.upload_part(part_num, part_data, upload_id, target_path_url_encode) 
                if not success:
                    print(f"Part {part_num} upload failed.")
                    return False
                print(f"Part {part_num} uploaded successfully.")
                 
        print("All parts uploaded successfully.")
        return True  # 所有分片上传成c
    # 合并分片
    def mergeSplit(self, local_path, target_path, upload_id, block_list):
        url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=create&access_token={self.access_token}"
        payload = {
        'path': f'{target_path}', 
        'size': f'{os.path.getsize(local_path)}',
        'rtype': 1,
        'isdir': 0,
        'uploadid': f'{upload_id}',
        'block_list': f'{json.dumps(block_list)}'
         }
        print("Merge Payload", payload)
        files = [

        ]
        headers = {
            "User-Agent": "pan.baidu.com"
        }
        
        req = requests.Request("POST", url, headers=headers, data=json.dumps(payload), files = files)
        print("req url", req.url)
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print("Metge Result:", response.text.encode('utf8'))

    def oneStageUpload(self, file_path, target_path):
        """
        
            单步上传: 路径只可以为 /apps/fileBrowser/
            
        """
        url = f"https://c3.pcs.baidu.com/rest/2.0/pcs/file?method=upload&access_token={self.access_token}&path={target_path}"
        payload = {}
        files = [
        ('file', open(file_path,'rb'))
        ]
        headers = {
        }
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print(response.text.encode('utf8'))
    def getFileUpload(self, file_path, target_path):
        """
        
        三行是分片上传
        
        """
        pre, block_list = self.preUpload(file_path, target_path)
        upload_info = self.getSplitUpload(pre, file_path, target_path)
        merge_result = self.mergeSplit(file_path, target_path, pre.get('uploadid'), block_list)
        print(merge_result.text)
    
    """
        路径只可以为/apps/fileBrowser/xxxx
    """
    def createFolder(self, path):
        url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=create&access_token={self.access_token}"
        payload = {'path': f'{path}',
        'rtype': '1',
        'isdir': '1'}
        files = [
        ]
        headers = {
        }
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print(response.text.encode('utf8'))
if __name__ == "__main__":
    app_key = "Z8jyOkHkQSJkBCCs1itQMrOwk1mCHb4g"
    secret_key = "uZzRjDmkTsspXeNWRc5l3VgpDkAlllix"
    sign_key = "$C3RVxW65GXrxKxS@dgE+bquK5gmRc!+"
    app_id = "97411691"
    bd = baidu(app_key, secret_key, sign_key, app_id)
    # response = str(bd.getFileList(" "))
    # response = json.loads(response)
    # response = bd.getFileInfo("test/inside/1.txt")
    # print(response)
    # response = bd.searchFile("AR7-35T", " ")
    # response = bd.getDownload("test/inside/1.txt")
    file_path = "/home/featurize/work/filebrowser/filebrowser/test.py"
    # target_path = {'path':'/test/aloha/test.py'}
    target_path = '/apps/fileBrowser/test.py'
    # target_path_url_encode = urlencode(target_path)[5:]
    # target_path_url_encode = target_path['path']
    # print(urlencode(target_path)[5:])
    # target_path = 'test/inside'
    # block_list = bd.getblockList(file_path)
    # print(response)
    # print(response.text)
    # print(json.dumps(block_list))
    # path=路径 前五个不要
    """
    pre, block_list = bd.preUpload(file_path, target_path_url_encode)
    upload_info = bd.getSplitUpload(pre, file_path, target_path_url_encode )
    merge_result = bd.mergeSplit(file_path, target_path_url_encode, pre.get('uploadid'), block_list)
    """
    # bd.getFileUpload(file_path, target_path)
    # bd.oneStageUpload(file_path, target_path)
    bd.createFolder("/apps/fileBrowser/test")

