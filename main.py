from flask import Flask, request
import tools

app = Flask(__name__)


@app.route('/weworkapi/', methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        msgsignatrue = request.args.get("msg_signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = request.args.get("echostr")
        is_able = tools.urlvary(msgsignatrue, timestamp, nonce, echostr)  # 通过参数msg_signature对请求进行校验，确认调用者的合法性
        if is_able:
            final = tools.decode_echo(echostr)  # 解密echostr参数得到消息内容
            return final  # 响应GET请求，响应内容为明文消息内容(不能加引号，不能带bom头，不能带换行符)
        else:
            return "e"
    else:
        msgsignatrue = request.args.get("msg_signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = tools.tiqu(request.data)  # 提取接收的消息包中的Encrypt参数
        is_able = tools.urlvary(msgsignatrue, timestamp, nonce, echostr)  # 通过参数msg_signature对请求进行校验，确认调用者的合法性
        if is_able:
            msgs = tools.decode_echo(echostr)
            sender, text = tools.find(msgs.decode("UTF-8"))
            content = "%s发送了：%s" % (tools.dic[sender], text)
            if text == 0:
                return msgs
            if sender == "成员1的UserId":
                err = tools.send_to("all", content)
            else:
                err = tools.send_to("成员1的UserId", content)
            app.logger.error("%s，返回码：%s" % (content, err))
            return msgs
        else:
            return "e"


if __name__ == '__main__':
    app.debug = True
    app.run()
