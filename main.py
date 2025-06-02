import os
import time
from telethon.sync import TelegramClient
from telethon.errors import ChannelPrivateError, UsernameInvalidError

# 读取环境变量
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
proxy_host = os.getenv("PROXY_HOST")
proxy_port = int(os.getenv("PROXY_PORT")) if os.getenv("PROXY_PORT") else None
channel_input = os.getenv("CHANNEL_INPUT")  # 频道用户名或链接
target_tag = os.getenv("TARGET_TAG")        # 搜索标签，如 #jinricp
message_limit = int(os.getenv("MESSAGE_LIMIT", 100))
download_dir = os.getenv("DOWNLOAD_DIR", "downloads")
phone = os.getenv("PHONE")                   # 登录手机号（首次登录用）
bot_token = os.getenv("BOT_TOKEN")           # 备用：Bot Token登录

proxy = ('socks5', proxy_host, proxy_port) if proxy_host and proxy_port else None

os.makedirs(download_dir, exist_ok=True)

_last_time = None
_last_bytes = 0

def progress_callback(current, total):
    global _last_time, _last_bytes
    now = time.time()
    if _last_time is None:
        _last_time = now
        _last_bytes = current
        speed_mbps = 0
    else:
        diff_time = now - _last_time
        diff_bytes = current - _last_bytes
        speed_bps = (diff_bytes * 8) / diff_time if diff_time > 0 else 0  # bits per second
        speed_mbps = speed_bps / 1_000_000  # Mbps
        _last_time = now
        _last_bytes = current

    percent = current * 100 / total if total else 0
    print(f"\r下载进度: {percent:.2f}% ({current}/{total} bytes) 速度: {speed_mbps:.2f} Mbps", end='', flush=True)

def main():
    global _last_time, _last_bytes

    session_name = "session"  # 会话文件名（会存为 session.session）

    with TelegramClient(session_name, api_id, api_hash, proxy=proxy) as client:
        # 检测是否已经授权（有session文件且有效）
        if not client.is_user_authorized():
            # 需要登录
            if bot_token:
                client.start(bot_token=bot_token)
            else:
                if phone is None:
                    # 运行环境无手机号环境变量，尝试交互输入
                    phone_input = input("请输入手机号（国际格式，+开头）: ")
                else:
                    phone_input = phone
                client.start(phone=phone_input)  # 会要求输入验证码并完成登录，会话文件保存

        try:
            # 获取频道实体
            if not channel_input:
                channel_input_local = input("请输入频道用户名或邀请链接（如 mychannel 或 https://t.me/xxxxx）：").strip()
            else:
                channel_input_local = channel_input

            entity = client.get_entity(channel_input_local)
            print(f"✅ 频道名称: {entity.title}")

            # 读取搜索标签
            if not target_tag:
                target_tag_local = input("请输入要搜索的视频标签（例如 #jinricp）：").strip()
            else:
                target_tag_local = target_tag

            print(f"开始从频道消息中查找包含标签 {target_tag_local} 的视频...")

            messages = client.iter_messages(entity, limit=message_limit)
            count = 0

            for msg in messages:
                caption = getattr(msg, 'caption', '') or ''
                text = getattr(msg, 'text', '') or ''
                content = caption + text

                if msg.video and target_tag_local in content:
                    original_name = msg.file.name if msg.file and msg.file.name else None
                    if original_name:
                        filename = os.path.join(download_dir, original_name)
                    else:
                        filename = os.path.join(download_dir, f"video_{msg.id}.mp4")

                    print(f"\n🎥 开始下载: {filename}")

                    # 重置速度统计
                    _last_time = None
                    _last_bytes = 0

                    msg.download_media(file=filename, progress_callback=progress_callback)
                    print()  # 换行防止进度覆盖
                    count += 1

            if count == 0:
                print("⚠️ 未找到带有指定标签的视频")
            else:
                print(f"\n✅ 下载完成！共下载 {count} 个视频")

        except ChannelPrivateError:
            print("❌ 无法访问频道。请确认已加入该频道且账号有权限访问。")
        except UsernameInvalidError:
            print("❌ 频道用户名无效，请确认输入正确。")
        except Exception as e:
            print(f"❌ 发生错误：{e}")

if __name__ == "__main__":
    main()
