FROM docker.kexie.space/wilinz/paddlepaddle-base:latest

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的 /app 目录中
COPY .. /app

RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 应用的端口
EXPOSE 5000

# 设置容器启动时的默认命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
