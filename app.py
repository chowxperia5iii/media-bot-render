import streamlit as st
import os
import subprocess

st.set_page_config(page_title="🇲🇾 雲端轉碼助手", layout="centered")
st.title("🇲🇾 雲端媒體下載器")

url = st.text_input("請輸入 YouTube/媒體網址:")
fmt = st.selectbox("選擇格式", ["1. 原始音訊下載 (不轉碼)", "2. 高品質 MP3 (256kbps)", "3. 高品質 M4A (256kbps)", "4. MP4 (影片)"])

if st.button("🚀 開始處理"):
    if url:
        with st.spinner("嘗試規避檢測中... 請稍候"):
            subprocess.run("pip install -U yt-dlp", shell=True)
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            
            if "1. 原始音訊下載" in fmt:
                target = "download.m4a"
                cmd = f'yt-dlp --user-agent "{ua}" -f "bestaudio/best" -o "{target}" "{url}"'
            elif "2. 高品質 MP3" in fmt:
                target = "download.mp3"
                cmd = f'yt-dlp --user-agent "{ua}" -f "bestaudio" --extract-audio --audio-format mp3 --audio-quality 256K -o "{target}" "{url}"'
            elif "3. 高品質 M4A" in fmt:
                target = "download.m4a"
                cmd = f'yt-dlp --user-agent "{ua}" -f "bestaudio" --extract-audio --audio-format m4a --audio-quality 256K -o "{target}" "{url}"'
            elif "4. MP4" in fmt:
                target = "download.mp4"
                cmd = f'yt-dlp --user-agent "{ua}" -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" --merge-output-format mp4 -o "{target}" "{url}"'
            
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if os.path.exists(target):
                with open(target, "rb") as f:
                    st.download_button("✅ 下載到手機", f, file_name=target)
                st.success("成功繞過檢測！")
            else:
                if "Sign in" in res.stderr:
                    st.error("❌ YouTube 依舊要求登錄。請考慮下載非 YouTube 影音。")
                else:
                    st.error(f"下載失敗: {res.stderr}")
    else:
        st.warning("請輸入有效網址")
