# Python 3 web server
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import strftime, gmtime
import subprocess

hostName = "192.168.1.65"

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://web_OpenWrt.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Hello world %s</p>" % strftime("%Y-%m-%d %H:%M:%S", gmtime()), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":
    serverPort = subprocess.run(["uci", "get", "webserver.server.port"], stdout=subprocess.PIPE, text=True, check=True)

    webServer = HTTPServer((hostName, int(serverPort.stdout)), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort.stdout))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
