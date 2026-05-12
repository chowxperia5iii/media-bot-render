import streamlit as st
import os
import subprocess

st.set_page_config(page_title="🇲🇾 雲端轉碼助手", layout="centered")
st.title("🇲🇾 雲端媒體下載器")

url = st.text_input("請輸入 YouTube/媒體網址:")
fmt = st.selectbox("選擇格式", ["MP4 (影片)", "MP3 (音訊)"])

if st.button("🚀 開始處理"):
    if url:
        with st.spinner("嘗試規避檢測中... 請稍候"):
            # 1. 更新 yt-dlp 
            subprocess.run("pip install -U yt-dlp", shell=True)
            
            output_tpl = "download.%(ext)s"
            # 2. 增加偽裝參數：--user-agent 和 --extractor-args
            ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
            
            if "MP4" in fmt:
                cmd = f'yt-dlp --user-agent "{ua}" --no-check-certificate -f "best" --merge-output-format mp4 -o "{output_tpl}" "{url}"'
                target = "download.mp4"
            else:
                cmd = f'yt-dlp --user-agent "{ua}" --no-check-certificate -x --audio-format mp3 -o "{output_tpl}" "{url}"'
                target = "download.mp3"
            
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if os.path.exists(target):
                with open(target, "rb") as f:
                    st.download_button("✅ 下載到手機", f, file_name=target)
                st.success("成功繞過檢測！")
            else:
                if "Sign in" in res.stderr:
                    st.error("❌ YouTube 依舊要求登錄。請考慮下載非 YouTube 平台的影片測試，或使用 Cookies 方案。")
                else:
                    st.error(f"下載失敗: {res.stderr}")
    else:
        st.warning("請輸入有效網址")
