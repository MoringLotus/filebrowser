"""认证模块"""
import _thread
import base64
import json
import logging
import os
import sys
import tempfile
import time
import uuid
from http.server import HTTPServer
from pathlib import Path
from typing import Callable, overload, List, Dict
from aliConfig import *
import coloredlogs
import qrcode
import qrcode_terminal
import requests
aligo_config_folder = Path.home().joinpath('.aligo')
aligo_config_folder.mkdir(parents=True, exist_ok=True)

class aliAuth:
    @overload
    def __init__(
            self,
            name: str = 'aligo',
            show: Callable[[str], None] = None,
            level=logging.DEBUG,
            proxies: Dict = None,
            port: int = None,
            request_failed_delay: float = 3,
            requests_timeout: float = None,
            request_interval: int = 0,
    ):
        """扫描二维码登录"""
     # noinspection PyPep8Naming,SpellCheckingInspection
    def __init__(
            self, name: str = 'aligo',
            refresh_token: str = None,
            show: Callable[[str], None] = None,
            level: int = logging.DEBUG,
            proxies: Dict = None,
            port: int = None,
            request_failed_delay: float = 3,
            requests_timeout: float = None,
            re_login: bool = True,
            request_interval: int = 0,
    ):
        """登录验证
        :param name: (可选, 默认: aligo) 配置文件名称, 便于使用不同配置文件进行身份验证
        :param refresh_token:
        :param show: (可选) 显示二维码的函数
        :param level: (可选) 控制控制台输出
        :param proxies: (可选) 自定义代理 [proxies={"https":"localhost:10809"}],支持 http 和 socks5（具体参考requests库的用法）
        :param port: (可选) 开启 http server 端口，用于网页端扫码登录. 提供此值时，将不再弹出或打印二维码
        :param request_failed_delay: 请求失败后，延迟时间，单位：秒
        :param requests_timeout: same as requests timeout
        :param login_timeout: 登录超时时间，单位：秒
        :param re_login: refresh_token 失效后是否继续登录（弹出二维码或邮件，需等待） fix #73
        :param request_interval: 每次请求等待的时间，避免请求频繁触发风控
        """
        self._name_name = name
        self._name = aligo_config_folder.joinpath(f'{name}.json')
        self._port = port
        self._webServer: HTTPServer = None  # type: ignore
        
        self.log = logging.getLogger(name)
        self._request_failed_delay = request_failed_delay
        self._requests_timeout = requests_timeout
        self._re_login = re_login
        self._request_interval = request_interval
        self._refresh_token = None
        fmt = f'%(asctime)s.%(msecs)03d {name}.%(levelname)s %(message)s'

        coloredlogs.install(
            level=level,
            logger=self.log,
            milliseconds=True,
            datefmt='%X',
            fmt=fmt
        )

        #
        self.session = requests.session()
        self.session.trust_env = False
        self.session.proxies = proxies
        self.session.headers.update(UNI_HEADERS)

        self.token: Optional[Token] = None
        if os.name == 'nt':
            self._os_name = 'Windows 操作系统'
            show = show or self._show_qrcode_in_window
        elif sys.platform.startswith('darwin'):
            self._os_name = 'MacOS 操作系统'
            show = show or self._show_qrcode_in_window
        else:
            self._os_name = '类 Unix 操作系统'
            show = show or self._show_console
        self.log.info(self._os_name)
        self._show = show
        self._x_device_id = None

        
            
            
    
            
    def get(self, path: str, host: str = API_HOST, params: dict = None, headers: dict = None) -> requests.Response:
        """..."""
        return self.request(method='GET', url=host + path, params=params, headers=headers)

    def post(self, path: str, host: str = API_HOST, params: dict = None, headers: dict = None,
             data: dict = None, body: dict = None, ignore_auth: bool = False) -> requests.Response:
        """..."""
        if ignore_auth:
            if headers is None:
                headers = {}
            headers['Authorization'] = None
        return self.request(method='POST', url=host + path, params=params,
                            data=data, headers=headers, body=body)

    @staticmethod
    def _show_console(qr_link: str) -> str:
        """
        在控制台上显示二维码
        :param qr_link: 二维码链接
        :return: NoReturn
        """
        qr_img = qrcode.make(qr_link)

        # try open image
        # 1.
        qr_img.show()

        # show qrcode on console
        # 2.
        qrcode_terminal.draw(qr_link)

        # save image to file
        # 3.
        qrcode_png = tempfile.mktemp('.png')
        qr_img.save(qrcode_png)
        return qrcode_png

    @staticmethod
    def _show_qrcode_in_window(qr_link: str):
        """
        通过 *.png 的关联应用程序显示 qrcode
        :param qr_link: 二维码链接
        :return: NoReturn
        """
        # show qrcode in windows & macOS
        qr_img = qrcode.make(qr_link)
        qr_img.show()

    def _show_qrcode_in_web(self, qr_link: str):
        """浏览器显示二维码"""
        qr_img = qrcode.make(qr_link)
        qr_img.get_image()
        qr_img_path = tempfile.mktemp()
        qr_img.save(qr_img_path)
        # noinspection PyTypeChecker
        self._webServer = HTTPServer(('0.0.0.0', self._port), LoginServer)
        self._webServer.qrData = open(qr_img_path, 'rb').read()
        os.remove(qr_img_path)
        try:
            self._webServer.serve_forever()
        except OSError:
            self._webServer.shutdown()
            pass

    def _send_email(self, qr_link: str):
        """发送邮件"""
        qr_img = qrcode.make(qr_link)
        qr_img.get_image()
        qr_img_path = tempfile.mktemp()
        qr_img.save(qr_img_path)
        qr_data = open(qr_img_path, 'rb').read()
        send_email(
            self._email.email, self._name_name, self._email.content, qr_data,
            self._email.user, self._email.password, self._email.host, self._email.port
        )
        os.remove(qr_img_path)
        self.log.info(f'登录二维码已发送至 {self._email.email}')

    def _log_response(self, response: requests.Response):
        """打印响应日志"""
        self.log.info(
            f'{response.request.method} {response.url} {response.status_code} {len(response.content)}'
        )

    def device_logout(self):
        return self.post(USERS_V1_USERS_DEVICE_LOGOUT)

    def _login(self):
        """登录"""
        self.log.info('开始登录')
        response = self._login_by_qrcode()

        if response.status_code != 200:
            self.log.error('登录失败')
            self.raise_error_log(response)

        bizExt = response.json()['content']['data']['bizExt']
        bizExt = base64.b64decode(bizExt).decode('gb18030')

        # 获取解析出来的 refreshToken, 使用这个token获取下载链接是直链, 不需要带 referer header
        refresh_token = json.loads(bizExt)['pds_login_result']['refreshToken']
        self._refresh_token(refresh_token, True)

    def _login_by_qrcode(self) -> requests.Response:
        """二维码登录"""
        self.session.get(AUTH_HOST + V2_OAUTH_AUTHORIZE, params={
            'login_type': 'custom',
            'response_type': 'code',
            'redirect_uri': 'https://www.aliyundrive.com/sign/callback',
            'client_id': CLIENT_ID,
            'state': r'{"origin":"file://"}',
            # 'state': '{"origin":"https://www.aliyundrive.com"}',
        }, stream=True).close()

        #
        session_id = self.session.cookies.get('SESSIONID')
        self.log.debug(f'SESSIONID {session_id}')

        response = self.session.get(
            PASSPORT_HOST + NEWLOGIN_QRCODE_GENERATE_DO, params=UNI_PARAMS
        )
        self._log_response(response)
        data = response.json()['content']['data']

        qr_link = data['codeContent']

        # 开启服务
        #if self._port or self._email:
        if self._port:
                # noinspection HttpUrlsUsage
                self.log.info(f'请访问 http://<YOUR_IP>:{self._port} 扫描二维码')
                _thread.start_new_thread(self._show_qrcode_in_web, (qr_link,))
            #if self._email:
            #   self._send_email(qr_link)
        else:
            self.log.info('等待扫描二维码，扫码结束后关闭二维码窗口')
            #self._show(qr_link)
            qrcode_png = self._show(qr_link)
            if qrcode_png:
                self.log.info(f'二维码图片文件 {qrcode_png}')

        while True:
            response = self.session.post(
                PASSPORT_HOST + NEWLOGIN_QRCODE_QUERY_DO,
                data=data, params=UNI_PARAMS
            )
            login_data = response.json()['content']['data']
            # noinspection PyPep8Naming
            qrCodeStatus = login_data['qrCodeStatus']
            # noinspection SpellCheckingInspection
            if qrCodeStatus == 'NEW':
                pass
            elif qrCodeStatus == 'SCANED':
                self.log.info('已扫描 等待确认')
            elif qrCodeStatus == 'CONFIRMED':
                self.log.info(f'已确认')
                if self._port:
                    try:
                        self.session.get(f'http://localhost:{self._port}/close')
                    except requests.exceptions.ConnectionError:
                        pass
                return response
            else:
                self.log.warning('未知错误 可能二维码已经过期')
                if self._webServer:
                    self._webServer.shutdown()
                self.raise_error_log(response)
            time.sleep(3)
            

if __name__ == '__main__':
    authtest = aliAuth()
    authtest._login()
    

