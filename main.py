import os
import time
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import ChannelPrivateError, UsernameInvalidError

# 加载 .env 文件（可选）
load_dotenv()

# 环境变量读取
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
proxy_host = os.getenv("PROXY_HOST")
proxy_port = int(os.getenv("PROXY_PORT")) if os.getenv("PROXY_PORT") else None

channel_input = os.getenv("CHANNEL_INPUT")
if not channel_input:
    raise ValueError("❌ 未设置频道用户名或链接，请设置 CHANNEL_INPUT 环境变量")

target_tag = os.getenv("TARGET_TAG", "#mychannel")

# 设置代理（如有）
proxy = ('socks5', proxy_host, proxy_port) if proxy_host and proxy_port else None

# 下载目录
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)

# 下载速度计算变量
_last_time = None
_last_bytes = 0

def progress_callback(current, total):
    global _last_time, _last_bytes
    现在 = time.time()
    if _last_time is None:
        _last_time = now
        _last_bytes = current
        speed_mbps = 0
    else:
        diff_time = now - _last_time
        diff_bytes = current - _last_bytes
        speed_bps = (diff_bytes * 8) / diff_time if diff_time > 0 else 0
        speed_mbps = speed_bps / 1_000_000
        _last_time = now
        _last_bytes = current

    percent = current * 100 / total if total else 0
    print(f"\r下载进度: {percent:.2f}% ({current}/{total} bytes) 速度: {speed_mbps:.2f} Mbps", end='', flush=True)

# 主逻辑
with TelegramClient("session", api_id, api_hash, proxy=proxy) as client:
    try:
        entity = client.get_entity(channel_input)
        print(f"✅ 频道名称: {entity.title}")
        print(f"📌 频道 ID: -100{entity.id}")

        messages = client.iter_messages(entity, limit=message_limit)

        count = 0

        for msg in messages:
            caption = getattr(msg, 'caption', '') or ''
            text = getattr(msg, 'text', '') or ''
            content = caption + text

            if msg.video and target_tag in content:
                original_name = msg.file.name if msg.file and msg.file.name else None
                filename = os.path.join(download_dir, original_name or f"video_{msg.id}.mp4")

                print(f"\n🎥 开始下载: {filename}")
                # 重置下载速度计算
                _last_time = None
                _last_bytes = 0
                msg.download_media(file=filename, progress_callback=progress_callback)
                print()
                count += 1

        if count == 0:
            print("⚠️ 未找到带有指定标签的视频")
        else:
            print(f"\n✅ 下载完成！共下载 {count} 个视频")

    except ChannelPrivateError:
        print("❌ 无法访问频道。请确认你已加入该频道且账号有权限访问。")
    except UsernameInvalidError:
        print("❌ 频道用户名无效，请确认输入正确。")
    except Exception as e:
        print(f"❌ 发生错误：{e}")
