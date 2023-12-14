import socket
import time


class HTTPClient:
    HTTP_PORT = 80

    def __init__(self, host: str, path_to_resourse: str, method: str, request_body: str, headers: dict, timeout: float):
        self.host = host
        self.method = method
        self.request_body = request_body
        self.headers = headers
        self.timeout = timeout
        self.path_to_resourse = path_to_resourse

    def collect_request(self) -> bytes:
        request = f"{self.method} {self.path_to_resourse} HTTP/1.1\r\n"
        request += f"Host: {self.host}\r\n"
        request += self.get_headers_str()
        request += self.request_body
        return request.encode("utf-8")

    def get_headers_str(self) -> str:
        result = ''
        for name, value in self.headers.items():
            result += f"{name}: {value}\r\n"
        result += "\r\n"
        return result

    def create_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect((self.host, self.HTTP_PORT))
        return sock

    def send_request(self, sock: socket.socket):
        request = self.collect_request()
        sock.sendall(request)

    def get_responce_headers(self, socket: socket.socket):
        responce_headers = b''
        body_prefix = b''
        is_all_data_collected = False
        while True:
            responce_headers_chunk = socket.recv(1024)
            responce_headers += responce_headers_chunk
            if len(responce_headers_chunk) < 1024:
                is_all_data_collected = True
                break
            if b'\r\n\r\n' in responce_headers_chunk:
                break
        headers_prefix = responce_headers.split(b'\r\n\r\n')
        responce_headers = headers_prefix[0] + b'\r\n\r\n'
        body_prefix = headers_prefix[1]
        return is_all_data_collected, responce_headers, body_prefix

    def get_content_length(self, responce_headers: bytes):
        decoded = responce_headers.decode()
        if "Content-Length: " in decoded:
            length = int(decoded.split('Content-Length: ')[1].split('\r\n')[0])
            return length
        return None

    def get_responce_body(self, socket: socket.socket):
        while True:
            chunk = socket.recv(4096)
            yield chunk
            time.sleep(0.05)
            if len(chunk) < 4096:
                break

    def run(self):
        response = b''
        body = b''
        with self.create_socket() as socket:
            try:
                self.send_request(socket)
                is_all_data_collected, responce_headers, body_prefix = self.get_responce_headers(
                    socket)
                body += body_prefix
                content_length = self.get_content_length(responce_headers)
                if is_all_data_collected:
                    return (responce_headers + body_prefix).decode("utf-8")
                packet_length_generator = self.get_responce_body(socket)
                if not content_length:
                    for chunk in packet_length_generator:
                        body += chunk
                    print(
                        "Cannot make progress bar as the server doesn't give onformation about data_length")
                else:
                    recieved_length = len(body_prefix)
                    for chunk in packet_length_generator:
                        body += chunk
                        recieved_length += len(chunk)
                        HTTPClient._print_overwrite(
                            HTTPClient.get_progress(recieved_length, content_length))

            except TimeoutError as e:
                response = b"Socket timeout exeeded, data wasn't collected successfuly"
            response = responce_headers + body
            return response.decode("utf-8")

    @staticmethod
    def get_progress(current_length, max_length):
        percentage = max_length / current_length
        return f"downloading progress: {round(percentage, 2) * 100}%\r"

    @staticmethod
    def _print_overwrite(content):
        print(content, end='\r', flush=True)

    '''def make_request(self) -> str:
        response = b""
        request = self.collect_request()
        with self.create_socket() as socket:
            socket.sendall(request)
            try:
                while True:
                    chunk = socket.recv(4096)
                    response += chunk
                    if len(chunk) < 4096:
                        break
            except Exception as e:
                response = b"Socket timeout exeeded, data wasn't collected successfuly"

        return response.decode("utf-8")'''
