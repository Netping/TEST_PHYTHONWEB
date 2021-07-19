# Python 3 web server
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import strftime, gmtime
import subprocess
from threading import Thread

hostName = "192.168.1.65"

class StoppableHTTPServer(HTTPServer):
    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            print("StoppableHTTPServer === KeyboardInterrupt")
            pass
        finally:
            # Clean-up server (close socket, etc.)
            self.server_close()
            print("Server stopped.")

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

    webServer = StoppableHTTPServer((hostName, int(serverPort.stdout)), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort.stdout))
    thread = Thread(None, webServer.run)
    thread.start()

    try:
        thread.join()
    except KeyboardInterrupt:
        print("__main__ === KeyboardInterrupt")

# Shutdown server
    webServer.shutdown()
    thread.join()
    print("FINITO a la comedy")