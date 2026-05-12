#!/bin/bash

echo "🔍 開始診斷雲端下載器環境..."
echo "--------------------------------"

# 1. 檢查關鍵文件是否存在
files=("app.py" "Dockerfile" "requirements.txt")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ 找到 $file"
    else
        echo "❌ 缺失 $file ！正在重新生成..."
    fi
done

# 2. 自動修正 Dockerfile (確保帶有 FFmpeg 和正確的 Port)
cat << 'DOCKER' > Dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port", "10000", "--server.address", "0.0.0.0"]
DOCKER
echo "✅ Dockerfile 已校準 (包含 FFmpeg)"

# 3. 檢查 GitHub 連接狀態
echo "--------------------------------"
echo "📡 檢查 GitHub 推送狀態..."
git status

# 4. 一鍵推送到 GitHub
echo "--------------------------------"
echo "📤 正在將最新修正推送到 GitHub..."
git add .
git commit -m "System diagnosis and auto-fix"
git push origin master

echo "--------------------------------"
echo "🎉 診斷與修復完成！"
echo "📢 現在請回到 Render 頁面觀看日誌 (Logs)。"
