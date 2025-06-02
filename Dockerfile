# 使用官方 Python 3.11 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装依赖
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY main.py ./
COPY .env ./  # 如果你想把 .env 直接放镜像里

# 设置容器启动命令，允许传递命令行参数
ENTRYPOINT ["python", "main.py"]
CMD []
