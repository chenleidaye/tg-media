import os
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

api_id = int(os.getenv("API_ID") or input("请输入 API_ID: "))
api_hash = os.getenv("API_HASH") or input("请输入 API_HASH: ")
phone = os.getenv("PHONE") or input("请输入手机号（含国家码，如 +86...）: ")
session_name = os.getenv("SESSION_NAME", "session")

client = TelegramClient(session_name, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    code = input("请输入你收到的验证码: ")
    try:
        client.sign_in(phone, code)
    except SessionPasswordNeededError:
        password = input("你开启了两步验证，请输入密码: ")
        client.sign_in(password=password)

print(f"✅ 登录成功，session 文件已保存为 {session_name}.session")
client.disconnect()
