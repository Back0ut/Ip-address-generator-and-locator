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
            ip_parts = []
            
            for _ in range(4):
                rand_num = randint(0, 2)
                
                ip_parts.append(str(randint(0, 255))) if rand_num == 0 else \
                ip_parts.append(str(randint(0, 99))) if rand_num == 1 else ip_parts.append(str(randint(0, 9)))
            
            new_ip = '.'.join(ip_parts)
            
            if new_ip not in GenerateIp.ips:
                return new_ip

    def GetGeolocation(self, ip: str) -> tuple[str, str]:
        while True:
            try:
                response = get(f'http://ipinfo.io/{ip}/json')
                if response.status_code == 200:
                    data = response.json()
                    city, country = data.get('city', 'Unknown'), data.get('country', 'Unknown')
                    
                    return city, country
                
                else:
                    print(f"Error: Received status code {response.status_code}")
                    ip = self.GenerateNewIp()
            
            except RequestException as exc:
                print(f"Request failed: {exc}")
                ip = self.GenerateNewIp()

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
def generate_ips():
    ip_addresses = []
    
    for _ in range(randint(5, 10)):
        new_ip = GenerateIp()
        ip_addresses.append({'ip': new_ip.ip, 'city': new_ip.city, 'country': new_ip.country})
    
    return jsonify(ip_addresses)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
