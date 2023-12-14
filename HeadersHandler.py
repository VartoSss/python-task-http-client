import base64

class HeadersHandler:
    USER_AGENTS = {
        "desktop": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "iphone": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/119.0.6045.109 Mobile/15E148 Safari/604.1",
        "android_phone": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.66 Mobile Safari/537.36"
    }

    def __init__(self):
        self._headers = {}

    def add_user_headers(self, user_headers: dict):
        self._headers = {**user_headers}

    def add_cookie_headers(self, cookies: dict):
        cookie_str = '; '.join([f'{key}={value}' for key, value in cookies.items()])
        self._headers['Cookie'] = cookie_str

    def add_basic_auth_header(self, credentials: str):
        base64_credentials = base64.b64encode(credentials.encode()).decode()
        basic_auth_value = f"Basic {base64_credentials}"
        self._headers['Authorization'] = basic_auth_value

    def add_user_agents_header_from_list(self, user_agent_shortcut) -> bool:
        if user_agent_shortcut in self.USER_AGENTS:
            self._headers['User-Agent'] = self.USER_AGENTS[user_agent_shortcut]
            return True
        return False

    def get_headers(self):
        return self._headers