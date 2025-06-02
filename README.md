# Telegram Video Downloader

基于 [Telethon](https://github.com/LonamiWebs/Telethon) 的 Telegram 视频下载器，通过标签从指定频道批量下载视频，支持 Docker 一键部署，支持速率显示与原始文件名保存。

## ✨ 功能特性

- ✅ 根据标签从频道中批量下载视频
- ✅ 支持原始文件名保存
- ✅ 支持下载速率实时显示（Mbps）
- ✅ 支持自定义下载数量
- ✅ 支持 Docker 容器后台运行
- ✅ 自动使用 `.env` 或环境变量配置
- ✅ 支持使用 `.session` 文件免交互登录


## 环境变量配置

| 变量名            | 说明                | 示例                                                           | 必须             |
| -------------- | ----------------- | ------------------------------------------------------------ | -------------- |
| API\_ID        | Telegram API ID   | 1234567                                                      | 是              |
| API\_HASH      | Telegram API HASH | abcd1234efgh5678                                             | 是              |
| PHONE          | 登录手机号，国际格式（首次登录）  | +8613812345678                                               | 否（首次登录必填）      |
| BOT\_TOKEN     | Bot 令牌，替代手机号登录    | 123456\:ABC-DEF1234                                          | 否              |
| PROXY\_HOST    | 代理服务器地址           | 127.0.0.1                                                    | 否              |
| PROXY\_PORT    | 代理端口              | 7890                                                         | 否              |
| CHANNEL\_INPUT | 频道用户名或邀请链接        | mychannel 或 [https://t.me/mychannel](https://t.me/mychannel) | 是              |
| TARGET\_TAG    | 搜索的视频标签           | #jinricp                                                     | 是              |
| MESSAGE\_LIMIT | 最大拉取消息数           | 100                                                          | 否，默认100        |
| DOWNLOAD\_DIR  | 视频下载目录            | downloads                                                    | 否，默认 downloads |
| SESSION_NAME  | 会话文件名           | session                                                    | 否，默认 downloads |

🧪 示例输出

```bash
---
✅ 频道名称: 今日资源
📌 频道 ID: -1001234567890

🎥 开始下载: downloads/video.mp4
下载进度: 87.23% (16343298/18728393 bytes) 速度: 6.34 Mbps
✅ 下载完成！共下载 5 个视频
````

## 📦 使用方式

### 一、Python 本地运行

#### 1. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt
````

### 2. 创建 .env 文件

```bash
API_ID=你的API_ID
API_HASH=你的API_HASH
CHANNEL_INPUT=频道用户名或邀请链接（如 jinricp 或 https://t.me/xxxx）
TARGET_TAG=#视频标签
MESSAGE_LIMIT=要扫描的消息数量（可选，默认200）
SESSION_NAME=session
````

### 3. 运行
```bash
python main.py
````

二、生成 Telegram 登录会话（可选）
你可以通过以下脚本生成 .session 文件以便免交互使用：

```bash
python generate_session.py
````

环境变量支持：
```bash
API_ID=xxx
API_HASH=xxx
PHONE=+86手机号
SESSION_NAME=session
````


🐳 Docker 使用

##1. 构建镜像（本地开发用）

```bash
docker build -t telegram-video-downloader .
````


## 2.运行
```bash
docker run -d --name tvd \                            # 后台运行容器，命名为 tvd
  -e API_ID=xxxx \                                    # 设置 Telegram 的 API_ID（必须在 https://my.telegram.org 获取）
  -e API_HASH=xxxx \                                  # 设置 Telegram 的 API_HASH
  -e CHANNEL_INPUT=abcd \                             # 要爬取的频道用户名或邀请链接，例如 'abcd' 或 'https://t.me/xxxx'
  -e TARGET_TAG=#abcd \                               # 要匹配的标签，只有带此标签的视频才会被下载
  -e MESSAGE_LIMIT=200 \                              # 最多从频道中读取多少条消息（避免过多遍历）
  -e PROXY_HOST=your.proxy.ip \                       # 设置 SOCKS5 代理地址（可选）
  -e PROXY_PORT=10808 \                               # 设置 SOCKS5 代理端口（可选）
  -v /downloads:/app/downloads \                      # 将宿主机的 /downloads 映射为容器内的下载目录 /app/downloads
  gvddf/telegram-video-downloader                     # 使用你发布的镜像 gvddf/telegram-video-downloader
````


 # 🔐 如果未提前生成 .session，首次运行将失败，请先运行 generate_session.py 并挂载 .session 文件：


```bash

 -v /本地/session文件路径:/app/session.session

````
