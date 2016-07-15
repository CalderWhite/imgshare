from http.server import BaseHTTPRequestHandler, HTTPServer
import time, os, base64, json, datetime, calendar

hostName = os.getenv("127.0.0.1", "0.0.0.0")
hostPort = os.getenv("8080", 8080)
binaryData = {
    'gif' : 'image/gif',
    'png' : 'image/gif',
    'ico' : 'image/icon',
    'jpg' : 'image/jpg',
    'otf' : 'font/opentype'
}
textData = {
    'html' : 'text/html',
    'css' : 'text/css',
    'js' : 'text/js',
    'json' : 'application/json'
}
def currentTime():
    x = datetime.datetime.now()
    retstr = str(x.day) + "-" + calendar.month_name[x.month] + "-" + str(x.year) + "_" + str(x.hour) + ":" + str(x.minute) + ":" + str(x.second)
    return retstr
class MyServer(BaseHTTPRequestHandler):
    def userUpload(self):
        # gather user info
        userIp = self.headers["x-forwarded-for"]
        fileName = self.headers["dataFileName"]
        raw = open('userData/IpList.json','r').read()
        users = json.loads(raw)
        user = users[userIp]
        user["uploads"] += 1
        user["last_active"] = currentTime()
        wh = open('userData/IpList.json','w')
        wh.write(json.dumps(users, indent=4, sort_keys=True))
        open(user["root_path"] + "/" + fileName,'a')
        body = self.getBody()
        # we load the body, now we need to decode it and write the binary data to the image cache
        fh = open(user["root_path"] + "/" + fileName, "wb")
        fh.write(base64.b64decode(body.decode('utf-8')))
        fh.close()
        pass
    def createUser(self):
        userIp = self.headers["x-forwarded-for"]
        raw = open('userData/IpList.json','r').read()
        users = json.loads(raw)
        users[userIp] = {
            "root_path" : "userData/userFiles/" + userIp.replace(".","-"),
            "last_active" : currentTime(),
            "uploads" : 0
        }
        os.makedirs("userData/userFiles/" + userIp.replace(".","-"))
        wf = open('userData/IpList.json','w')
        jsonStr = json.dumps(users, indent=4, sort_keys=True)
        wf.write(jsonStr)
        pass
    def getUser(self):
        # check if the user (ip) has previously requested
        userIp = self.headers["x-forwarded-for"]
        raw = open('userData/IpList.json','r').read()
        users = json.loads(raw)
        if users.__contains__(userIp):
            return users[userIp]
        else:
            return False
    def getFile(self,path,text=True):
        global r
        r = None
        try:
            if text:
                r = open(path,'r').read()
            else:
                r = open(path,'rb').read()
        except FileNotFoundError:
            return None
        return r
    def do_normalGET(self):
        # if the request has no path, send the default html page
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(open("pages/redirect.html",'r').read(), "utf-8"))
    def do_mobileGET(self):
        # if the request has no path, send the default html page
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(open("pages/redirectMobile.html",'r').read(), "utf-8"))
    def do_GET(self):
        global binaryData
        global textData
        if self.path[1:] == "favicon.ico":
            self.send_response(406)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("No favicon.ico",'utf-8'))
        # ---------------------------
        if self.headers.__contains__("custom-action"):
            pass
        else:
            #print(self.headers)
            if self.path == "/":
                # check if mobile (though this isn't the most thorough way, it's the quickest)
                mobile = self.headers['user-agent']
                print(mobile)
                if mobile.lower().find("mobile") > -1:
                    self.do_mobileGET()
                    pass
                else:
                    self.do_normalGET()
                #self.wfile.write(bytes(open("Client/Client.html",'r').read(), "utf-8"))
                #print(bytes(open("Client/Client.html",'r').read(), "utf-8"))
            else:
                print("Got File Req")
                # here's where we find the file type, so we know if we need to read bytes or text
                fileName = self.path.split("/")[-1]
                ending = fileName.split(".")[-1]
                rat = True
                # if the suffix to the file (after the .) matches one of the suffixes in the dictionary at the top of this file,
                # it sets the variable rat (for read as text) to False, so the file will be read as binary
                for i in binaryData:
                    if ending == i:
                        rat = False
                f = self.getFile(self.path[1:],text=rat)
                if f == None:
                    self.simpleResponse(404,'text/html',open("pages/notFound.html").read())
                else:
                    # find out if the data is a supported type
                    mime_type = None
                    for i in binaryData:
                        if ending == i:
                            mime_type = binaryData[i]
                            break;
                    if mime_type == None:
                        for i in textData:
                            if ending == i:
                                mime_type = textData[i]
                                break;
                    if mime_type == None:
                        self.simpleResponse(400,"text/plain","Error 400, Bad request (Unknown Data type)")
                    else:
                        self.send_response(200)
                        self.send_header("Content-type",mime_type)
                        self.end_headers()
                        if rat:
                            self.wfile.write(bytes(f,'utf-8'))
                        else:
                            self.wfile.write(f)
    def getBody(self):
        content_len = int(self.headers['content-length'])
        data = self.rfile.read(content_len)
        return data
    def simpleResponse(self,code,data_type,data,encoding="utf-8"):
        # this way you can send a simple message without headers or anything, saving a couple lines of code.
        # this is mainly for things like a response to a post request (just requires a simple message)
        self.send_response(code)
        self.send_header("Content-type", data_type)
        self.end_headers()
        self.wfile.write(bytes(data,encoding))
    def do_POST(self):
        action = self.path[1:]
        if action == "Client/clientUpload" or "Client/clientUpload":
            if self.headers.__contains__("dataFileName") == False:
                self.simpleResponse(400,"text/plain","Error 400, Bad request (dataFileName header missing)")
            else:
                user = self.getUser()
                if user == False:
                    self.createUser()
                    self.userUpload()
                else:
                    self.userUpload()
            #print("succesfully recived image post. Now stored in imgCache.png")
            self.simpleResponse(200,'text/plain',"Succesfully recived image post.")

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

myServer.serve_forever()
print(time.asctime(), "Server Ends - %s:%s" % (hostName, hostPort))