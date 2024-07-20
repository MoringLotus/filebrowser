

def getFileUpload(self, upload_url, local_path):
    local_path = '/test/1.txt'
    # 读取文件内容
    with open(file_path, 'rb') as file:
        file_content = file.read()
    # 定义请求的 URL 和头部信息
    url = 'https://cn-beijing-data.aliyundrive.net/ssed035v%2F1232775%2F63db7b45cac3ae9ec9bc4889b8464c82c247d479%2F63db7b459958f0a7af8f4bc88407b0505afb7df8?partNumber=1&security-token=CAIS%2BgF1q6Ft5B2yfSjIr5eAeomAv7lZgfepWBfpkVRge9cZ14DSsDz2IHFPeHJrBeAYt%2FoxmW1X5vwSlq5rR4QAXlDfNS6LBD7eqVHPWZHInuDox55m4cTXNAr%2BIhr%2F29CoEIedZdjBe%2FCrRknZnytou9XTfimjWFrXWv%2Fgy%2BQQDLItUxK%2FcCBNCfpPOwJms7V6D3bKMuu3OROY6Qi5TmgQ41Uh1jgjtPzkkpfFtkGF1GeXkLFF%2B97DRbG%2FdNRpMZtFVNO44fd7bKKp0lQLukMWr%2Fwq3PIdp2ma447NWQlLnzyCMvvJ9OVDFyN0aKEnH7J%2Bq%2FzxhTPrMnpkSlacGoABSMP1VoMchlg3%2BcK8b9Z8w2TnorSIfXyEJietSKoHjhlKPM6x%2BgvUni75uVxjrQ4bu%2BPQTKuj7RT6draXxIdC9l2AIuX%2BIWRe1frVkXmVIq%2BPkz0hBdWNKXA5Dzs6TphxcqwQJfVLiIBZmQHzLL5ijoswP728b4ybXYvNEZ5DQP4%3D&uploadId=12A91A279FCC49DA83ACE66B2AEDB4E2&x-oss-access-key-id=STS.NT5134Rfx65BZ1XuT5wX58EyR&x-oss-expires=1675331925&x-oss-signature=CHaqx2V62six%2Fg%2B3bI%2FMr6Y9j824GQr5JttMm5VxEKQ%3D&x-oss-signature-version=OSS2'
    headers = {
        'Content-Type': 'application/octet-stream',
        'x-oss-access-key-id': 'STS.NT5134Rfx65BZ1XuT5wX58EyR',
        'x-oss-expires': '1675331925',
        'x-oss-signature': 'CHaqx2V62six%2Fg%2B3bI%2FMr6Y9j824GQr5JttMm5VxEKQ%3D',
        'x-oss-signature-version': 'OSS2'
    }

    # 发送 PUT 请求
    response = requests.put(url, data=file_content, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        print("文件上传成功")
        print(response)
    else:
        print("文件上传失败，状态码：", response.status_code)
        

# ?????
if __name__ == "__main__":
    url = 'https://cn-beijing-data.aliyundrive.net/ssed035v%2F1232775%2F63db7b45cac3ae9ec9bc4889b8464c82c247d479%2F63db7b459958f0a7af8f4bc88407b0505afb7df8?partNumber=1&security-token=CAIS%2BgF1q6Ft5B2yfSjIr5eAeomAv7lZgfepWBfpkVRge9cZ14DSsDz2IHFPeHJrBeAYt%2FoxmW1X5vwSlq5rR4QAXlDfNS6LBD7eqVHPWZHInuDox55m4cTXNAr%2BIhr%2F29CoEIedZdjBe%2FCrRknZnytou9XTfimjWFrXWv%2Fgy%2BQQDLItUxK%2FcCBNCfpPOwJms7V6D3bKMuu3OROY6Qi5TmgQ41Uh1jgjtPzkkpfFtkGF1GeXkLFF%2B97DRbG%2FdNRpMZtFVNO44fd7bKKp0lQLukMWr%2Fwq3PIdp2ma447NWQlLnzyCMvvJ9OVDFyN0aKEnH7J%2Bq%2FzxhTPrMnpkSlacGoABSMP1VoMchlg3%2BcK8b9Z8w2TnorSIfXyEJietSKoHjhlKPM6x%2BgvUni75uVxjrQ4bu%2BPQTKuj7RT6draXxIdC9l2AIuX%2BIWRe1frVkXmVIq%2BPkz0hBdWNKXA5Dzs6TphxcqwQJfVLiIBZmQHzLL5ijoswP728b4ybXYvNEZ5DQP4%3D&uploadId=12A91A279FCC49DA83ACE66B2AEDB4E2&x-oss-access-key-id=STS.NT5134Rfx65BZ1XuT5wX58EyR&x-oss-expires=1675331925&x-oss-signature=CHaqx2V62six%2Fg%2B3bI%2FMr6Y9j824GQr5JttMm5VxEKQ%3D&x-oss-signature-version=OSS2'
    print(url)