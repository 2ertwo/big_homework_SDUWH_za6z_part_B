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
        is_able = tools.urlvary(msgsignatrue, timestamp, nonce, echostr)
        if is_able:
            final = tools.decode_echo(echostr)
            return final
        else:
            return "e"
    else:
        msgsignatrue = request.args.get("msg_signature")
        timestamp = request.args.get("timestamp")
        nonce = request.args.get("nonce")
        echostr = tools.tiqu(request.data)
        is_able = tools.urlvary(msgsignatrue, timestamp, nonce, echostr)
        if is_able:
            msgs = tools.decode_echo(echostr)
            text = tools.find(msgs.decode("UTF-8"))
            app.logger.error(text)
            err = tools.send_to("BaiJinFan", text)
            app.logger.error(err)
            return msgs
        else:
            tools.send_to("BaiJinFan", msgsignatrue)
            tools.send_to("BaiJinFan", timestamp)
            tools.send_to("BaiJinFan", nonce)
            tools.send_to("BaiJinFan", echostr)
            return "e"


if __name__ == '__main__':
    app.debug = True
    app.run()
