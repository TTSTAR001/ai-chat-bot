# 导入依赖
import dashscope
from http import HTTPStatus

# ===================== 配置区（替换为你自己的API信息）=====================
dashscope.api_key = "sk-424ec6820bb544cc90ef03bc8bba4e88"  # 此处务必替换成个人密钥
# 预设3种对话角色
ROLE_LIST = {
    "1": {"name": "智能助手", "prompt": "你是专业、严谨的AI助手，简洁回答问题"},
    "2": {"name": "学习导师", "prompt": "你是学习辅导老师，耐心讲解知识点"},
    "3": {"name": "幽默好友", "prompt": "你是风趣幽默的朋友，聊天轻松有趣"}
}
# 全局变量：上下文记忆、当前角色、对话记录
chat_history = []
current_role_prompt = ROLE_LIST["1"]["prompt"]

# ===================== 功能1：多轮对话（上下文记忆）=====================
def chat_with_llm(user_input):
    """调用大模型，实现带上下文的多轮对话"""
    global chat_history
    # 拼接角色人设 + 历史对话 + 当前提问
    messages = [{"role": "system", "content": current_role_prompt}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_input})

    # 调用大模型接口
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=messages,
        result_format="message"
    )

    if response.status_code == HTTPStatus.OK:
        answer = response.output.choices[0].message.content
        # 保存本轮对话到上下文
        chat_history.append({"role": "user", "content": user_input})
        chat_history.append({"role": "assistant", "content": answer})
        return answer
    else:
        return f"请求失败：{response.code} - {response.message}"

# ===================== 功能2：切换对话角色 =====================
def switch_role(role_num):
    """切换AI对话人设"""
    global current_role_prompt
    if role_num in ROLE_LIST:
        current_role_prompt = ROLE_LIST[role_num]["prompt"]
        print(f"\n✅ 已切换为：{ROLE_LIST[role_num]['name']}")
    else:
        print("\n❌ 输入序号无效")

# ===================== 功能3：对话记录 查看 / 清空 =====================
def save_chat_log():
    """保存对话到本地文件"""
    with open("chat_log.txt", "w", encoding="utf-8") as f:
        for msg in chat_history:
            f.write(f"{msg['role']}：{msg['content']}\n")

def show_chat_log():
    """查看历史对话记录"""
    print("\n===== 历史对话记录 =====")
    if not chat_history:
        print("暂无对话记录")
        return
    for msg in chat_history:
        for msg in chat_history:
            print(f"{msg['role']}：{msg['content']}")

def clear_chat_log():
    """清空对话记录+上下文"""
    global chat_history
    chat_history = []
    # 清空本地文件
    with open("chat_log.txt", "w", encoding="utf-8") as f:
        f.write("")
    print("\n✅ 对话记录已全部清空")

# ===================== 主程序入口 =====================
def main():
    print("===== AI基础对话机器人 =====")
    print("功能说明：")
    print("1. 正常输入文字开始聊天（支持多轮对话）")
    print("2. 输入【角色】切换AI人设")
    print("3. 输入【记录】查看历史对话")
    print("4. 输入【清空】删除所有记录")
    print("5. 输入【退出】结束程序\n")

    while True:
        user_text = input("你：")
        # 退出程序
        if user_text == "退出":
            save_chat_log()
            print("👋 程序已退出，对话已自动保存")
            break
        # 切换角色
        elif user_text == "角色":
            print("\n可选角色：")
            for k, v in ROLE_LIST.items():
                print(f"{k}. {v['name']}")
            select = input("请输入角色序号：")
            switch_role(select)
        # 查看记录
        elif user_text == "记录":
            show_chat_log()
        # 清空记录
        elif user_text == "清空":
            clear_chat_log()
        # 正常聊天（核心对话功能）
        else:
            ai_answer = chat_with_llm(user_text)
            print(f"AI：{ai_answer}")

if __name__ == "__main__":
    main()