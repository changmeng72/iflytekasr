# -*- encoding:utf-8 -*-

import sys
import hashlib
from hashlib import sha1
import hmac
import base64
from socket import *
import json, time, threading
from websocket import create_connection
import websocket
from urllib.parse import quote
import logging
from audioInf import audioInf 
import datetime


from contentAnalysis import xfcontentAnalysis

# reload(sys)
# sys.setdefaultencoding("utf8")
logging.basicConfig()

base_url = "ws://rtasr.xfyun.cn/v1/ws"
app_id = "5f2b191e"
api_key = "08d4feff6b534d526def26063ce0b8a4"
file_path = r"./test_1.pcm"

pd = "edu"

end_tag = "{\"end\": true}"

 

class Client():
    def __init__(self):
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.start = False
        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()
    
    def reconnect(self):
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        self.start = False
        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
         

    def send(self, file_path):
        
        file_object = open(file_path, 'rb')
        while self.start==False :
            time.sleep(1)
        try:
            index = 1
            seconds = time.time()
            print("Seconds since epoch =", seconds)
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                start = datetime.datetime.now()
                self.ws.send(chunk)
                end = datetime.datetime.now()
                #print(end-start)

                index += 1
                #time.sleep(0.04)
                if index%100 == 0 :
                    seconds = time.time()
                    print("Seconds since epoch =", seconds);
                
        finally:
            file_object.close()

        self.ws.send(bytes(end_tag.encode('utf-8')))
        print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    break
                result_dict = json.loads(result)
                # 解析结果
                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)
                    self.start = True

                if result_dict["action"] == "result":
                    result_1 = result_dict
                    # result_2 = json.loads(result_1["cn"])
                    # result_3 = json.loads(result_2["st"])
                    # result_4 = json.loads(result_3["rt"])
                    #print("rtasr result: " + result_1["data"])
                    #print(type(result_1["data"]))
                    res = xfcontentAnalysis(json.loads(result_1["data"])).decode()
                    if res != "":
                        print("final result time: =", time.time());
                        print(res)

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    self.reconnect()
        
                    #return
        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")


if __name__ == '__main__':
    client = Client()
    if len(sys.argv)==1:
        myaudio = audioInf(ws=client.ws)
        threading.Thread(target=myaudio.rtAsr).start()
        a = input("to stop input any key + enter:")
        print("after sleep, now stop")
        myaudio.stop()
    else:
        client.send(sys.argv[1])
    
