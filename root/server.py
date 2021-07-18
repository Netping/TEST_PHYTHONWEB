# Python 3 web server
from http.server import BaseHTTPRequestHandler, HTTPServer
from time import strftime, gmtime
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from multiprocessing import Process
from multiprocessing.sharedctypes import Value

hostName = "192.168.1.65"

PATH_UCI_FILE = "/etc/config/webserver"
change_param = False

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://web_OpenWrt.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Hello world %s</p>" % strftime("%Y-%m-%d %H:%M:%S", gmtime()), "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

class  MyHandler(FileSystemEventHandler):
    def  on_modified(self,  event):
        global change_param
        print("IN on_modified")
        if event.src_path == PATH_UCI_FILE:
            change_param = True
            print("on_modified = ", change_param)

def track_file_change(fl_change_param):
    global change_param

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler,  PATH_UCI_FILE,  recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(3)
            if change_param == True:
                change_param = False
                fl_change_param.value = 1
                print("NEW process CLEAR True")
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, PATH_UCI_FILE, recursive=False)
    observer.start()

    while True:
        try:
            pass
        except  KeyboardInterrupt:
            observer.stop()
        observer.join()

    exit()





    fl_change_param = Value('i', 0)

    serverPort = subprocess.run(["uci", "get", "webserver.server.port"], stdout=subprocess.PIPE, text=True, check=True)
    webServer = HTTPServer((hostName, int(serverPort.stdout)), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort.stdout))

    proc = Process(target=track_file_change, args=(fl_change_param,))
    proc.start()

    while proc.is_alive():
        print("Tracking file UIC in work")
#        print(change_param)
        if fl_change_param.value == 1:
            fl_change_param.value = 0
            print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        time.sleep(1)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

