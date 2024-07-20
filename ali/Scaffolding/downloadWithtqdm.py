import requests
from tqdm import tqdm

def download_file(url, file_path):
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

# URL 需要替换为实际的下载链接
download_url = 'https://cn-beijing-data.aliyundrive.net/5f906f299d7233373007492b80dca7708f34422b%2F5f906f297acd4900c8d24820be78b0c530657183?callback=eyJjYWxsYmFja1VybCI6Imh0dHA6Ly9iajI5LmFwaS1ocC5hbGl5dW5wZHMuY29tL3YyL2ZpbGUvZG93bmxvYWRfY2FsbGJhY2siLCJjYWxsYmFja0JvZHkiOiJodHRwSGVhZGVyLnJhbmdlPSR7aHR0cEhlYWRlci5yYW5nZX1cdTAwMjZidWNrZXQ9JHtidWNrZXR9XHUwMDI2b2JqZWN0PSR7b2JqZWN0fVx1MDAyNmRvbWFpbl9pZD0ke3g6ZG9tYWluX2lkfVx1MDAyNnVzZXJfaWQ9JHt4OnVzZXJfaWR9XHUwMDI2ZHJpdmVfaWQ9JHt4OmRyaXZlX2lkfVx1MDAyNmZpbGVfaWQ9JHt4OmZpbGVfaWR9XHUwMDI2dmVyc2lvbj0ke3g6dmVyc2lvbn0iLCJjYWxsYmFja0JvZHlUeXBlIjoiYXBwbGljYXRpb24veC13d3ctZm9ybS11cmxlbmNvZGVkIiwiY2FsbGJhY2tTdGFnZSI6ImJlZm9yZS1leGVjdXRlIiwiY2FsbGJhY2tGYWlsdXJlQWN0aW9uIjoiaWdub3JlIn0%3D&callback-var=eyJ4OmRvbWFpbl9pZCI6ImJqMjkiLCJ4OnVzZXJfaWQiOiJhM2Y5NWI5ZWExNjg0YTAwOGJjYmJiMGI5MTAxYzRkNSIsIng6ZHJpdmVfaWQiOiI1Mzc5NDI1NCIsIng6ZmlsZV9pZCI6IjY2OTlkZGJlMGQ3NGRmZWY0NTZiNDZhYjk4YjgzMGViNjZiMDZjOGEiLCJ4OnZlcnNpb24iOiJ2MyJ9&di=bj29&dr=53794254&f=6699ddbe0d74dfef456b46ab98b830eb66b06c8a&response-content-disposition=attachment%3B%20filename%2A%3DUTF-8%27%271GB.bin&security-token=CAISvgJ1q6Ft5B2yfSjIr5bdOu38p71Jxo%2BRdFfVpngEetpUoa6elDz2IHhMf3NpBOkZvvQ1lGlU6%2Fcalq5rR4QAXlDfNTnuD32yq1HPWZHInuDox55m4cTXNAr%2BIhr%2F29CoEIedZdjBe%2FCrRknZnytou9XTfimjWFrXWv%2Fgy%2BQQDLItUxK%2FcCBNCfpPOwJms7V6D3bKMuu3OROY6Qi5TmgQ41Uh1jgjtPzkkpfFtkGF1GeXkLFF%2B97DRbG%2FdNRpMZtFVNO44fd7bKKp0lQLs0ARrv4r1fMUqW2X543AUgFLhy2KKMPY99xpFgh9a7j0iCbSGyUu%2FhcRm5sw9%2Byfo34lVYneo7nf3QnWi4IClLcc%2BmqdsRIvJzWstJ7Gf9LWqChvSgk4TxhhcNFKSTQrInFCB0%2BcRObJl16icWihuvXtuMkagAGzHPl%2Fcw14yttcPcJ64zstnUlfK5li36wHHBZUIa4o6cqU2%2ByYOTO3mqtHVJoVt1zXrC9bUfH9b%2FvTQ5%2FkWTj%2FPQx%2Btl%2BUEfpEo%2BhsMRFuyiUJnHdWQ9ZLUL1UlQ%2Fc9sb9APKhc8amtk2hyMIPq7UrLwaldBhfQGeUlj5osucHRiAA&u=a3f95b9ea1684a008bcbbb0b9101c4d5&x-oss-access-key-id=STS.NUhqWHJbhqMzvqdBxQvUxNk5v&x-oss-expires=1721361439&x-oss-signature=tiU%2FiTElmb0iNp1oF3LEAQzM%2BMgGj%2BqqK1E84Gp%2FZMc%3D&x-oss-signature-version=OSS2'
file_path = '1GB.bin'

download_file(download_url, file_path)