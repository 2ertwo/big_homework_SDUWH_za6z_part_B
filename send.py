import tools
name_to_id = {"白锦帆": "BaiJinFan",
              "宫晨风": "GongChenFeng",
              "李晓峰": "lintong",
              "孙阳": "8bff448a58c8315307d6d1761b0ed267",
              "王倩怡学姐": "Rearrange"}
while True:
    print("发送消息(退出请输入0)")
    print("-" * 50)
    target = input("请输入要发送的目标：")
    if target == "0":
        break
    target = name_to_id[target]
    text = input("请输入要发送的文本：")
    err = tools.send_to(target, text)
    if err == "0" or err is None:
        print("发送成功，返回码：0。")
    else:
        print("发送失败，返回码：%s" % err)
    print("-" * 50)
