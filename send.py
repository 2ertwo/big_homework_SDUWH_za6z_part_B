import tools
name_to_id = {"成员1的姓名": "成员1的UserId",
              "成员2的姓名": "成员2的UserId"}
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
