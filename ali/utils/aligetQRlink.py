
def aligetQRlink(self):
        self.session.get(AUTH_HOST + V2_OAUTH_AUTHORIZE, params={
            'login_type': 'custom',
            'response_type': 'code',
            'redirect_uri': 'https://www.aliyundrive.com/sign/callback',
            'client_id': CLIENT_ID,
            'state': r'{"origin":"file://"}',
            # 'state': '{"origin":"https://www.aliyundrive.com"}',
        }, stream=True).close()
        session_id = self.session.cookies.get('SESSIONID')
        self.log.debug(f'SESSIONID {session_id}')

        response = self.session.get(
            PASSPORT_HOST + NEWLOGIN_QRCODE_GENERATE_DO, params=UNI_PARAMS
        )
        self._log_response(response)
        data = response.json()['content']['data']

        qr_link = data['codeContent']