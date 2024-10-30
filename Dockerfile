FROM python:3.10.15-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的 /app 目录中
COPY . /app

RUN apt update && apt-get install libgl1 libglib2.0-0 libgomp1 -y
# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的端口
EXPOSE 5000

# 设置容器启动时的默认命令
CMD ["python", "main.py"]
