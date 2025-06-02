# tg-media

用法示例
环境变量 .env 配置你的 API_ID、API_HASH、代理 PROXY_HOST 和 PROXY_PORT（如果有）：


API_ID=你的api_id
API_HASH=你的api_hash
PROXY_HOST=127.0.0.1
PROXY_PORT=7890
运行脚本

命令行参数方式：

python main.py -c mychannel -t "#jinricp" -d downloads
交互式输入（直接运行不带参数）：


python main.py
请输入频道用户名或邀请链接（如 mychannel 或 https://t.me/xxxxx）：mychannel
请输入要搜索的视频标签（例如 #jinricp）：#jinricp


docker run --rm -it \
  -e API_ID=你的api_id \
  -e API_HASH=你的api_hash \
  -e PROXY_HOST=127.0.0.1 \
  -e PROXY_PORT=7890 \
  telegram-video-downloader
