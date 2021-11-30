import hashlib
from base64 import b64decode
from Crypto.Cipher import AES  # 在Windows上应为Cryptodome
import socket
import struct
import xml.etree.cElementTree as ET
import requests
import re
corpId = ""  # 这里是你的企业ID
token = ""  # 这里是你自建应用的access_token
encodingAesKey = ""  # 这里是你自建应用的编码后的AesKey
ouraccess = ""  # 这里是你发送消息时用的access_token，第一次使用可留空
corpsecret = ""  # 这里是你应用的Secret
dic = {"成员1的UserId": "成员1的姓名",
       "成员2的UserId": "成员2的姓名",
       "成员3的UserId": "成员3的姓名",
       "成员4的UserId": "成员4的姓名",
       "成员5的UserId": "成员5的姓名"}


def urlvary(msgsignatrue, timestamp, nonce, echostr):  # 验证签名
    thelist = sorted([token, timestamp, nonce, echostr])  # 字典排序
    need = ""
    for i in range(4):
        need += thelist[i]  # 字符串拼接
    result = hashlib.sha1(need.encode("utf-8")).hexdigest()  # 取sha1
    if result == msgsignatrue:  # 判断签名是否相等
        return True
    else:
        return False


def decode_echo(sth):  # 解码消息体
    need_aes = b64decode(sth)  # 原消息base64解码
    aeskey = b64decode(encodingAesKey + "=")  # 先对编码后的AesKey进行b64解码
    aes = AES.new(aeskey, AES.MODE_CBC, aeskey[:16])
    plain_text = aes.decrypt(need_aes)  # 用AesKey解密文本
    content = plain_text[16:]  # 去除前面的随机数
    xml_len = socket.ntohl(struct.unpack("I", content[: 4])[0])  # 提取消息长度
    xml_content = content[4:xml_len+4]  # 提取xml消息
    from_receiveid = content[xml_len+4:]  # 提取receiveid
    return xml_content


def send_to(who, text):
    global ouraccess  # 声明全局变量
    url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + ouraccess  # 请求地址
    if who == "all":  # 判断发送目标
        target = "成员1id|成员2id|成员3id|成员4id|成员5id"  # 群发所有人
    else:
        target = who  # 单发某个人
    data = {
        "touser": target,
        "msgtype": "text",
        "agentid": 1000003,
        "text": {
                 "content": text
                },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0
        }  # 消息体
    req = requests.post(url, json=data)  # 发送Post请求
    errcode = re.findall(r"errcode\":(.+?),\"errmsg", req.text)[0]  # 提取返回码
    if errcode == "40014" or errcode == "42001":  # 40014和42001都代表access_token出问题
        ouraccess = get_access_token()  # 重新获取access_token
        send_to(who, text)  # 重新发送
    else:
        return errcode  # 返回返回码以供可能的Debug


def tiqu(str):  # 提取正文消息
    xml_tiqu = ET.fromstring(str)
    encrypt = xml_tiqu.find("Encrypt")
    return encrypt.text


def get_access_token():  # 获得access_token
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpId + '&corpsecret=' + corpsecret  # 构建url
    req = requests.get(url)  # 发送Get请求
    new = re.findall(r"access_token\":\"(.+?)\",\"expires_in", req.text)  # 提取返回的access_token
    return new[0]


def find(sth):
    text = [0]
    msg_type = re.findall(r"<MsgType><!\[CDATA\[(.+?)\]\]></MsgType>", sth)  # 提取信息类型参数
    sender = re.findall(r"<FromUserName><!\[CDATA\[(.+?)\]\]></FromUserName>", sth)  # 提取发送者参数
    if msg_type[0] != "text":
        text[0] = 0
    else:
        text = re.findall(r"<Content><!\[CDATA\[(.+?)\]\]></Content>", sth)  # 提取正文
    return sender[0], text[0]
