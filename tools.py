import hashlib
from base64 import b64decode
from Cryptodome.Cipher import AES  # 在Linux上应为Crypto
import socket
import struct
import xml.etree.cElementTree as ET
import requests
import re
# corpId = "ww3f0728af56e6f87c"
# token = "PVIqN3sRkFHYI"
# encodingAesKey = "1VPNUrpKMphkcTLyjo7sgYgcfQJ8cWPF5pq4DPifWHa"
# ouraccess = "KloHVTiqfaBBsITkjqxAzckFci_vauxm4q0O4eXPLRNqBRy_sVusJ9vHQkBXYcAYaGT0TOrdvPekweNS6Dua7k4sipCjKoaKy4icg-vz0205e0itUOreueitMYocMDs0T5HobDDjRfKg68gxBcC8-xlSrjN6Me55T-v7BL0a7LexRAkf4lUxU0L38ME4l2djlY7tvlKRimf0CudK8sbq5w"
corpId = "ww3f0728af56e6f87c"
corpsecret = "wd6WHoP9X_z7KqfNmVRPNC8UyHd8s_0CpxwQ4F9awJ4"
token = "Wvmtqi"
encodingAesKey = "cSsrSnv43DWGOCX75aagbdV5BcIk3cCBsu5IPV5J1Px"
ouraccess = " "
dic = {"BaiJinFan": "白锦帆",
    "GongChenFeng": "宫晨峰",
    "lintong": "李晓峰",
    "8bff448a58c8315307d6d1761b0ed267": "孙阳",
    "rearrange": "王婧怡学姐"}

def urlvary(msgsignatrue, timestamp, nonce, echostr):
    thelist = sorted([token, timestamp, nonce, echostr])
    need = ""
    for i in range(4):
        need += thelist[i]
    result = hashlib.sha1(need.encode("utf-8")).hexdigest()
    if result == msgsignatrue:
        return True
    else:
        return False


def decode_echo(sth):
    need_aes = b64decode(sth)
    aeskey = b64decode(encodingAesKey + "=")
    aes = AES.new(aeskey, AES.MODE_CBC, aeskey[:16])
    plain_text = aes.decrypt(need_aes)
    content = plain_text[16:]
    xml_len = socket.ntohl(struct.unpack("I", content[: 4])[0])
    xml_content = content[4:xml_len+4]
    from_receiveid = content[xml_len+4:]
    return xml_content


def send_to(who, text):
    global ouraccess
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + ouraccess
    if who == "all":
        target = "BaiJinFan|GongChenFeng|lintong|8bff448a58c8315307d6d1761b0ed267"
    else:
        target = who
    data ={
        "touser": target,
        "msgtype": "text",
        "agentid": 1000003,
        "text": {
                 "content": text
                },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0
        }
    req = requests.post(url, json=data)
    errcode = re.findall(r"errcode\":(.+?),\"errmsg", req.text)[0]
    if errcode == "40014" or errcode == "42001":
        ouraccess = get_access_token()
        send_to(who, text)
    else:
        return errcode


def tiqu(str):
    xml_tiqu = ET.fromstring(str)
    encrypt = xml_tiqu.find("Encrypt")
    return encrypt.text


def get_access_token():
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpId + '&corpsecret=' + corpsecret
    req = requests.get(url)
    new = re.findall(r"access_token\":\"(.+?)\",\"expires_in", req.text)
    return new[0]


def find(sth):
    text = [0]
    msg_type = re.findall(r"<MsgType><!\[CDATA\[(.+?)\]\]></MsgType>", sth)
    sender = re.findall(r"<FromUserName><!\[CDATA\[(.+?)\]\]></FromUserName>", sth)
    if msg_type[0] != "text":
        text[0] = sth
    else:
        text = re.findall(r"<Content><!\[CDATA\[(.+?)\]\]></Content>", sth)
    return "%s发送了%s" % (sender[0], text[0])


if __name__ == '__main__':
    print(urlvary("477715d11cdb4164915debcba66cb864d751f3e6", "1409659813", "1372623149", "RypEvHKD8QQKFhvQ6QleEB4J58tiPdvo+rtK1I9qca6aM/wvqnLSV5zEPeusUiX5L5X/0lWfrf0QADHHhGd3QczcdCUpj911L3vg3W/sYYvuJTs3TUUkSUXxaccAS0qhxchrRYt66wiSpGLYL42aM6A8dTT+6k4aSknmPj48kzJs8qLjvd4Xgpue06DOdnLxAUHzM6+kDZ+HMZfJYuR+LtwGc2hgf5gsijff0ekUNXZiqATP7PF5mZxZ3Izoun1s4zG4LUMnvw2r+KqCKIw+3IQH03v+BCA9nMELNqbSf6tiWSrXJB3LAVGUcallcrw8V2t9EL4EhzJWrQUax5wLVMNS0+rUPA3k22Ncx4XXZS9o0MBH27Bo6BpNelZpS+/uh9KsNlY6bHCmJU9p8g7m3fVKn28H3KDYA5Pl/T8Z1ptDAVe0lXdQ2YoyyH2uyPIGHBZZIs2pDBS8R07+qN+E7Q=="))
