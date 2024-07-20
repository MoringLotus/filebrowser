from requests import request
from ..core import aliConfig
from ..config.aliConfig import OAUTH_AUTHORIZE, OPEN_API_HOST
"""
para:
    client_id: App Id 每个应用唯一
    _port:     服务端口??
    
method:
    QRLogin:
        return: 

"""
def aliLogin(self):
    def __init__(self, client_id : str):
        self.client_id = ?
        self.session   = requests.session()
        # 设置在类的入口？？？
        self._port     = "二维码服务端口待设定"
    def QRlogin(self):
        while True:
            response = self.session.post(
                OPEN_API_HOST + OAUTH_AUTHORIZE_QRCODE,
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
                pass
    
    

if __name__ == "__main__":
    aL = aliLogin()
    
