import json
import http.client

# 配置区
API_KEY = "sk-424ec6820bb544cc90ef03bc8bba4e88"
MODEL = "qwen-turbo"

# 预设角色
ROLE_LIST = {
    "1": {"name": "智能助手", "prompt": "你是专业、严谨的AI助手，简洁回答问题"},
    "2": {"name": "学习导师", "prompt": "你是学习辅导老师，耐心讲解知识点"},
    "3": {"name": "幽默好友", "prompt": "你是风趣幽默的朋友，聊天轻松有趣"}
}

chat_history = []
current_role_prompt = ROLE_LIST["1"]["prompt"]

def chat_with_llm(user_input):
    global chat_history
    messages = [{"role": "system", "content": current_role_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    conn = http.client.HTTPSConnection("dashscope.aliyuncs.com")
    payload = json.dumps({
        "model": MODEL,
        "input": {"messages": messages},
        "parameters": {"result_format": "message"}
    })
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    conn.request("POST", "/api/v1/services/aigc/text-generation/generation", payload, headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    if "output" in data and "choices" in data["output"]:
        answer = data["output"]["choices"][0]["message"]["content"]
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": answer})
        return answer
    else:
        return f"请求失败：{data.get('code', '未知错误')} - {data.get('message', '')}"

def switch_role(role_num):
    global current_role_prompt
    if role_num in ROLE_LIST:
        current_role_prompt = ROLE_LIST[role_num]["prompt"]
        print(f"\n✅ 已切换为：{ROLE_LIST[role_num]['name']}")
    else:
        print("\n❌ 输入序号无效")

def save_chat_log():
    with open("chat_log.txt", "w", encoding="utf-8") as f:
        for msg in chat_history:
            f.write(f"{msg['role']}：{msg['content']}\n")

def show_chat_log():
    print("\n===== 历史对话记录 =====")
    if not chat_history:
        print("暂无对话记录")
        return
    for msg in chat_history:
        print(f"{msg['role']}：{msg['content']}")

def clear_chat_log():
    global chat_history
    chat_history = []
    with open("chat_log.txt", "w", encoding="utf-8") as f:
        f.write("")
    print("\n✅ 对话记录已全部清空")

def main():
    print("===== AI基础对话机器人（无依赖版）=====")
    print("功能说明：")
    print("1. 正常输入文字开始聊天（支持多轮对话）")
    print("2. 输入【角色】切换AI人设")
    print("3. 输入【记录】查看历史对话")
    print("4. 输入【清空】删除所有记录")
    print("5. 输入【退出】结束程序\n")

    while True:
        user_text = input("你：")
        if user_text == "退出":
            save_chat_log()
            print("👋 程序已退出，对话已自动保存")
            break
        elif user_text == "角色":
            print("\n可选角色：")
            for k, v in ROLE_LIST.items():
                print(f"{k}. {v['name']}")
            select = input("请输入角色序号：")
            switch_role(select)
        elif user_text == "记录":
            show_chat_log()
        elif user_text == "清空":
            clear_chat_log()
        else:
            ai_answer = chat_with_llm(user_text)
            print(f"AI：{ai_answer}")

if __name__ == "__main__":
    main()