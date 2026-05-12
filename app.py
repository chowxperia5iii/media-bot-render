import streamlit as st
import os
import subprocess

st.set_page_config(page_title="🇲🇾 雲端轉碼助手", layout="centered")
st.title("🇲🇾 雲端媒體下載器")

url = st.text_input("請輸入 YouTube/媒體網址:")
fmt = st.selectbox("選擇格式", ["MP4 (影片)", "MP3 (音訊)"])

if st.button("🚀 開始處理"):
    if url:
        with st.spinner("雲端轉碼中... (使用 Cookies 授權中)"):
            # 確保環境有最新 yt-dlp
            subprocess.run("pip install -U yt-dlp", shell=True)
            
            output_tpl = "download.%(ext)s"
            # 增加 --cookies cookies.txt 參數來規避機器人檢測
            if "MP4" in fmt:
                cmd = f'yt-dlp --cookies cookies.txt -f "best" --merge-output-format mp4 -o "{output_tpl}" "{url}"'
                target = "download.mp4"
            else:
                cmd = f'yt-dlp --cookies cookies.txt -x --audio-format mp3 -o "{output_tpl}" "{url}"'
                target = "download.mp3"
            
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if os.path.exists(target):
                with open(target, "rb") as f:
                    st.download_button("✅ 下載到手機", f, file_name=target)
                st.success("處理成功！")
            else:
                st.error(f"下載失敗。原因：{res.stderr}")
    else:
        st.warning("請輸入有效網址")
