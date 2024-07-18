from flask import Flask, jsonify, render_template_string
from requests import RequestException, get as requests_get
from random import randint
import os

app = Flask(__name__)

class GenerateIp:
    ips = []

    private_ip_blocks: list = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255")
    ]

    def __init__(self) -> None:
        self.ip = self.GenerateNewIp()
        self.city, self.country = self.GetGeolocation(self.ip)
        
        GenerateIp.ips.append(self.ip)

    def GenerateNewIp(self) -> str:
        while True:
            ip_parts = [str(randint(1, 255)) for _ in range(4)]
            new_ip = '.'.join(ip_parts)
            
            if new_ip not in GenerateIp.ips and not self.is_PrivateIp(new_ip):
                return new_ip

    def is_PrivateIp(self, ip: str) -> bool:
        ip_int = int(''.join(f'{int(part):08b}' for part in ip.split('.')), 2)
        
        for block_start, block_end in GenerateIp.private_ip_blocks:
            def split_ip_ToBinary(start_or_end):
                return int(''.join(f'{int(part):08b}' for part in start_or_end.split('.')), 2)
            
            start_int = split_ip_ToBinary(block_start)
            end_int = split_ip_ToBinary(block_end)
            
            if start_int <= ip_int <= end_int:
                return True
        
        return False

    def GetGeolocation(self, ip: str) -> tuple[str, str]:
        try:
            response = requests_get(f'http://ip-api.com/json/{ip}')
            data = response.json()
            city, country = data.get('city', 'Unknown'), data.get('country', 'Unknown')
        
        except RequestException as exc:
            print(f"Error fetching data for IP {ip}: {exc}")
            city, country = 'Unknown', 'Unknown'

            if city == 'Unknown' and country == 'Unknown':
                GenerateIp.private_ip_blocks.append(self.ip)
        
        return city, countryclass GenerateIp:
    ips = []

    private_ip_blocks: list = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255")
    ]

    def __init__(self) -> None:
        self.ip = self.GenerateNewIp()
        self.city, self.country = self.GetGeolocation(self.ip)
        
        GenerateIp.ips.append(self.ip)

    def GenerateNewIp(self) -> str:
        while True:
            ip_parts = [str(randint(1, 255)) for _ in range(4)]
            new_ip = '.'.join(ip_parts)
            
            if new_ip not in GenerateIp.ips and not self.is_PrivateIp(new_ip):
                return new_ip

    def is_PrivateIp(self, ip: str) -> bool:
        ip_int = int(''.join(f'{int(part):08b}' for part in ip.split('.')), 2)
        
        for block_start, block_end in GenerateIp.private_ip_blocks:
            def split_ip_ToBinary(start_or_end):
                return int(''.join(f'{int(part):08b}' for part in start_or_end.split('.')), 2)
            
            start_int = split_ip_ToBinary(block_start)
            end_int = split_ip_ToBinary(block_end)
            
            if start_int <= ip_int <= end_int:
                return True
        
        return False

    def GetGeolocation(self, ip: str) -> tuple[str, str]:
        try:
            response = requests_get(f'http://ip-api.com/json/{ip}')
            data = response.json()
            city, country = data.get('city', 'Unknown'), data.get('country', 'Unknown')
        
        except RequestException as exc:
            print(f"Error fetching data for IP {ip}: {exc}")
            city, country = 'Unknown', 'Unknown'

            if city == 'Unknown' and country == 'Unknown':
                GenerateIp.private_ip_blocks.append(self.ip)
        
        return city, country

html_template = os.path.join('C:/Users/ABC/Desktop/VsCode Projects/Python Projects/Ip-address-Generator', 'Ip-Address-Generator-template.html')

@app.route('/')
def index() -> render_template_string:
    try:
        with open(html_template, 'r') as file:
            template = file.read()
    
    except FileNotFoundError:
        return 'Error: Template file not found', 500
    
    return render_template_string(template)

@app.route('/generate')
def generate_ips() -> jsonify:
    ip_addresses = []
    
    for _ in range(randint(5, 10)):
        new_ip = GenerateIp()
        ip_addresses.append({'ip': new_ip.ip, 'city': new_ip.city, 'country': new_ip.country})
    
    return jsonify(ip_addresses)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
