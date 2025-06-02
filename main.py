import os
import time
import argparse
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.errors import ChannelPrivateError, UsernameInvalidError

load_dotenv()

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

    percent = (current / total * 100) if total else 0
    print(f"\r下载进度: {percent:.2f}% ({current}/{total} bytes) 速度: {speed_mbps:.2f} Mbps", end='', flush=True)

def main():
    parser = argparse.ArgumentParser(description="批量下载 Telegram 频道带标签的视频")
    parser.add_argument("-c", "--channel", type=str, help="频道用户名或邀请链接")
    parser.add_argument("-t", "--tag", type=str, help="要搜索的视频标签，如 #jinricp")
    parser.add_argument("-d", "--dir", type=str, default="downloads", help="下载目录，默认downloads")
    parser.add_argument("--proxy_host", type=str, default=os.getenv("PROXY_HOST"), help="代理服务器地址")
    parser.add_argument("--proxy_port", type=int, default=int(os.getenv("PROXY_PORT") or 0), help="代理服务器端口")
    args = parser.parse_args()

    api_id = int(os.getenv("API_ID"))
    api_hash = os.getenv("API_HASH")
    proxy = None
    if args.proxy_host and args.proxy_port:
        proxy = ('socks5', args.proxy_host, args.proxy_port)

    if not args.channel:
        args.channel = input("请输入频道用户名或邀请链接（如 mychannel 或 https://t.me/xxxxx）：").strip()
    if not args.tag:
        args.tag = input("请输入要搜索的视频标签（例如 #jinricp）：").strip()

    os.makedirs(args.dir, exist_ok=True)

    global _last_time, _last_bytes
    _last_time = None
    _last_bytes = 0

    with TelegramClient("session", api_id, api_hash, proxy=proxy) as client:
        try:
            entity = client.get_entity(args.channel)
            print(f"✅ 频道名称: {entity.title}")
            print(f"📌 频道 ID: -100{entity.id}")

            messages = client.iter_messages(entity, limit=200)
            count = 0

            for msg in messages:
                caption = getattr(msg, 'caption', '') or ''
                text = getattr(msg, 'text', '') or ''
                content = caption + text

                if msg.video and args.tag in content:
                    original_name = msg.file.name if msg.file and msg.file.name else None
                    if original_name:
                        filename = os.path.join(args.dir, original_name)
                    else:
                        filename = os.path.join(args.dir, f"video_{msg.id}.mp4")

                    print(f"\n🎥 开始下载: {filename}")
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
            print("❌ 无法访问频道。请确认你已加入该频道且账号有权限访问。")
        except UsernameInvalidError:
            print("❌ 频道用户名无效，请确认输入正确。")
        except Exception as e:
            print(f"❌ 发生错误：{e}")

if __name__ == "__main__":
    main()
