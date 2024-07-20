# Filebrowser

## 功能

* 支持多种后端（本地、阿里云OSS、AWS、百度云盘、阿里云盘）
* 基本的文件操作（拷贝，移动，删除，重命名，新建文件夹）
* 不同后端支持跨后端文件拷贝和移动
* 文件下载（支持单个文件、文件夹、文件夹压缩后下载，压缩后下载支持断点续传）
* 文件上传（支持单个文件、文件夹，单个文件上传支持续传）
* 耗时的任务支持后台运行并且展示进度
* 长金文件类型的内容查看（图片、文本、音频、视频）

## 配置和系统状态

* 用户的认证信息。例如百度云、阿里云的配置信息
* 断点上传保存的文件碎片。
* 本地后端支持根目录的配置。
* 是否展示隐藏文件
* ...

## 设计

### File 类

File 表示任意一个文件，它是一个抽象类，有多种子类，每个子类对应一个后端，例如 **LcalFile**，**BaiduyunFile** 等。File 类提供了基本的文件操作接口，例如拷贝、移动、删除、重命名、新建文件夹等。

File 抽象类提供一个工厂方法 `from_str`，根据文件路径创建一个 File 对象。例如：

```Python
file: LocalFile = File.from_str("local:///path/to/file")
file: BaiduyunFile = File.from_str("baiduyun:///path/to/file")
file: AliyunFile = File.from_str("aliyun:///path/to/file")
file: HTTPFile = File.from_str("http:///path/to/file")
```

这样设计的目的是接口对于文件的描述都可以使用字符串的形式，接口可以统一，例如拷贝一个文件的接口可以是：

* POST /files/copy?src=local:///path/to/file&dest=baiduyun:///path/to/file

**File 接口**

| 方法 | 说明 |
| --- | --- |
| **stat() -> FileStat** | 获取文件的元信息（FileStr、大小、修改时间，是否是目录等） |
| **read() -> bytes** | 读取文件的 chunk bytes |
| **write(b: bytes) -> int** | 将一部分 bytes 写入文件 |
| **move(dest: str \| File) -> None** | 移动文件到 dest，如果是跨 backend 的移动，则实际上是执行 copy + delete 操作 |
| **delete() -> None** | 删除文件 |
| **copy(dest: str \| File) -> None** | 拷贝文件到 dest |
| **list_dir() -> list[FileStat]** | 列出文件夹下的文件，仅当当前文件是文件夹时有效，不是文件夹调用则报错 |

### API 接口

| API 接口 | 说明 |
| ---- | ---- |
| GET /files/list?path=[str] | 获取某个目录下的子文件，path 必须是一个目录，否则返回 422 |
| GET /files/stat?path=[str] | 获取某个文件的元信息 |
