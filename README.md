# Telegram 频道视频批量下载器

使用 Python 和 Telethon 库，从指定 Telegram 频道批量下载带指定标签的视频，支持代理和环境变量配置，适合 Docker 后台运行。

---

## 功能特点

- 支持通过频道用户名或邀请链接获取频道
- 支持按视频消息中指定标签筛选下载
- 保留视频原始文件名保存
- 支持 SOCKS5 代理
- 下载过程显示实时进度和速率（Mbps）
- 支持环境变量配置，方便 Docker 无人值守运行

---

## 环境变量配置

| 变量名        | 说明                             | 必填 | 示例           |
|---------------|----------------------------------|------|----------------|
| `API_ID`      | Telegram API ID                  | 是   | `1234567`      |
| `API_HASH`    | Telegram API Hash                | 是   | `abcdef123456` |
| `PROXY_HOST`  | SOCKS5 代理地址（可选）          | 否   | `127.0.0.1`    |
| `PROXY_PORT`  | SOCKS5 代理端口（可选）          | 否   | `7890`         |
| `CHANNEL_INPUT` | 频道用户名或完整邀请链接        | 是   | `mychannel` 或 `https://t.me/mychannel` |
| `TARGET_TAG`  | 视频消息中筛选的标签（可选）     | 否   | `#mychannel`     |
| `MESSAGE_LIMIT` | 最多拉取消息条数，默认 200 | 否  | `500` |

---

## 快速开始

### 1. 准备 `.env` 文件

```dotenv
API_ID=1234567
API_HASH=abcdef1234567890abcdef1234567890
PROXY_HOST=127.0.0.1
PROXY_PORT=7890
CHANNEL_INPUT=mychannel
TARGET_TAG=#jinricp
MESSAGE_LIMIT=500

如果不使用代理，PROXY_HOST 和 PROXY_PORT 可留空或不设置。

2. 运行脚本
python main.py
程序自动读取 .env，连接 Telegram，遍历频道最近 200 条消息，下载包含指定标签的视频文件。

Docker 使用示例
##构建镜像

docker build -t telegram-video-downloader .

docker run -d --name tvd \
  -e API_ID=1234567 \
  -e API_HASH=abcdef1234567890abcdef1234567890 \
  -e PROXY_HOST=127.0.0.1 \
  -e PROXY_PORT=7890 \
  -e CHANNEL_INPUT=mychannel \
  -e TARGET_TAG=#jinricp \
  -e MESSAGE_LIMIT=500 \
  -v $(pwd)/downloads:/app/downloads \
  telegram-video-downloader


查看日志
docker logs -f tvd
