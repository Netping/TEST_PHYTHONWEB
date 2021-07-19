# Python 3 web server
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import strftime, gmtime, sleep
import subprocess
from threading import Thread

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

def get_port():
    serverPort = subprocess.run(["uci", "get", "webserver.server.port"], stdout=subprocess.PIPE, text=True, check=True)
    return int(serverPort.stdout)

def run_server(host_name, port):
    webServer = StoppableHTTPServer((host_name, port), MyServer)
    print("Server started http://%s:%i" % (host_name, port))
    thread = Thread(None, webServer.run)
    thread.start()

    return webServer, thread

def stop_server(webServer, thread):
    webServer.shutdown()
    thread.join()
    print("Shutdown Thread")

if __name__ == "__main__":
    host_option = subprocess.run(["uci", "get", "network.lan.ipaddr"], stdout=subprocess.PIPE, text=True, check=True)
    hostname = host_option.stdout.rstrip()

    old_port = get_port()
    cur_port = old_port

    webServer, thread = run_server(hostname, cur_port)

    try:
        while True:
            cur_port = get_port()
            if cur_port != old_port:
                stop_server(webServer, thread)
                webServer, thread = run_server(hostname, cur_port)
                old_port = cur_port
            sleep(1)
    except KeyboardInterrupt:
        print("__main__ === KeyboardInterrupt")

    stop_server(webServer, thread)
    print("FINITO a la comedy")