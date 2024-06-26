from flask import Flask, jsonify, render_template_string
from requests import get, RequestException
from random import randint

app = Flask(__name__)

class GenerateIp:
    ips = []

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
        private_ip_blocks = [
            ("10.0.0.0", "10.255.255.255"),
            ("172.16.0.0", "172.31.255.255"),
            ("192.168.0.0", "192.168.255.255")
        ]

        ip_int = int(''.join(f'{int(part):08b}' for part in ip.split('.')), 2)
        
        for block_start, block_end in private_ip_blocks:
            start_int = int(''.join(f'{int(part):08b}' for part in block_start.split('.')), 2)
            end_int =   int(''.join(f'{int(part):08b}' for part in block_end.split('.')), 2)
            
            if start_int <= ip_int <= end_int:
                return True
        
        return False

    def GetGeolocation(self, ip: str) -> tuple[str, str]:
        try:
            response = get(f'http://ip-api.com/json/{ip}')
            data = response.json()
            print(data)
            city, country = data.get('city', 'Unknown'), data.get('country', 'Unknown')
        
        except RequestException as exc:
            print(f"Error fetching data for IP {ip}: {exc}")
            city, country = 'Unknown', 'Unknown'
        
        return city, country

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>IP Generator</title>
        </head>
        <body>
            <h1>Randomly Generated IP Addresses</h1>
            <button onclick="generateIps()">Generate IPs</button>
            <ul id="ip-list"></ul>
            <script>
                function generateIps() {
                    fetch('/generate_ips')
                        .then(response => response.json())
                        .then(data => {
                            const ipList = document.getElementById('ip-list');
                            ipList.innerHTML = '';
                            data.forEach(ip => {
                                const li = document.createElement('li');
                                li.textContent = `${ip.ip} - ${ip.city}, ${ip.country}`;
                                ipList.appendChild(li);
                            });
                        });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/generate_ips')
def generate_ips() -> jsonify:
    ip_addresses = []
    
    for _ in range(randint(5, 10)):
        new_ip = GenerateIp()
        ip_addresses.append({'ip': new_ip.ip, 'city': new_ip.city, 'country': new_ip.country})
    
    return jsonify(ip_addresses)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
