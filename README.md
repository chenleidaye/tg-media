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

---

## 📦 使用方式

### 一、Python 本地运行

#### 1. 安装依赖

```bash
python3 -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt


### 2. 创建 .env 文件
#
API_ID=你的API_ID
API_HASH=你的API_HASH
CHANNEL_INPUT=频道用户名或邀请链接（如 jinricp 或 https://t.me/xxxx）
TARGET_TAG=#视频标签
MESSAGE_LIMIT=要扫描的消息数量（可选，默认200）
SESSION_NAME=session

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

第一次运行时，你需要执行容器的交互式终端登录：

docker run -it --rm \
  -e API_ID=xxx \
  -e API_HASH=yyy \
  -v /path/to/session:/app/session \
  your-image-name python main.py
交互完成登录后，session.session 会保存在你本地的 /path/to/session 文件夹内。

后续启动容器时，挂载同一个目录即可实现无交互运行：
docker run -d --name tvd \
  -e API_ID=xxx \
  -e API_HASH=yyy \
  -e CHANNEL_INPUT=xxx \
  -e TARGET_TAG=#tag \
  -e MESSAGE_LIMIT=100 \
  -v /path/to/session:/app/session \
  -v /downloads:/app/downloads \
  your-image-name

docker run -d --name tvd \
  -e API_ID=xxx \
  -e API_HASH=yyy \
  -e CHANNEL_INPUT=xxx \
  -e TARGET_TAG=#tag \
  -e MESSAGE_LIMIT=100 \
  -v /path/to/session:/app/session \
  -v /downloads:/app/downloads \
  your-image-name

查看日志
docker logs -f tvd
