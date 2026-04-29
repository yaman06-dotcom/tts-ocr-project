import streamlit as st
import cv2
import numpy as np
from PIL import Image
import easyocr
from gtts import gTTS
import os
import time

@st.cache_resource
def load_reader():
    return easyocr.Reader(['ar', 'en'])

st.set_page_config(page_title="AI Journey: The Ultimate Visual Lab", layout="wide", page_icon="🚀")

# تنسيق CSS شامل لكل الميزات
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMarkdown, .stTitle, .stHeader { color: #e2e8f0 !important; }
    
    .step-box {
        background: #1e293b;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 40px;
        border-left: 8px solid #3b82f6;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    
    .logic-card {
        background: #0f172a;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
    }
    
    .highlight-blue { color: #60a5fa; font-weight: bold; }
    .highlight-green { color: #4ade80; font-weight: bold; }
    
    .code-window {
        background: #000;
        padding: 15px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        color: #4ade80;
        font-size: 0.9rem;
        margin-top: 15px;
        border: 1px solid #333;
    }
    
    .terminal-window {
        background-color: #000000;
        border-radius: 10px;
        border: 1px solid #333;
        padding: 20px;
        font-family: 'Courier New', Courier, monospace;
        margin: 10px 0;
        min-height: 250px;
    }
    
    .code-line { color: #4ade80; margin: 5px 0; font-size: 0.9rem; white-space: pre-wrap; }
    .cursor { display: inline-block; width: 8px; height: 15px; background: #4ade80; margin-left: 5px; animation: blink 1s infinite; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    
    .wave-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 3px;
        height: 80px;
        margin: 20px 0;
    }
    .wave-bar {
        width: 4px;
        background: #60a5fa;
        border-radius: 2px;
        height: 10px;
    }
    .active-wave .wave-bar {
        animation: sound-wave 1s infinite ease-in-out;
    }
    @keyframes sound-wave {
        0%, 100% { height: 10px; }
        50% { height: 60px; }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("مشروع TTS")
st.markdown("مرحباً بك في العرض الجامعي الشامل. سنقوم الآن بتشريح كل مرحلة برمجية وبصرية بالتفصيل.")

# 1. مرحلة المدخلات
st.header("📸 1. استقبال المصفوفة الأصلية (RGB Input)")
uploaded_file = st.file_uploader("ارفع الصورة لبدء الرحلة التعليمية الشاملة...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    st.markdown("<div class='step-box'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1.2])
    with col1:
        st.image(image_rgb, use_container_width=True, caption="الصورة الأصلية (3 قنوات ألوان)")
    with col2:
        st.subheader("البيانات الخام")
        st.markdown("""
        <div class='logic-card'>
        هذه هي نقطة البداية. الصورة عبارة عن مصفوفة بكسلات تحمل قيم الألوان (الأحمر، الأخضر، الأزرق). <br>
        <span class='highlight-blue'>التحدي:</span> كثرة الألوان تمثل ضجيجاً للنظام، لذا يجب تبسيطها.
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. تبسيط القنوات (Grayscale)
    st.header("🔘 2. تبسيط القنوات (Grayscale Transformation)")
    st.markdown("<div class='step-box' style='border-left-color: #fbbf24;'>", unsafe_allow_html=True)
    col3, col4 = st.columns([1, 1.2])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    with col3:
        st.image(gray, use_container_width=True, caption="قناة واحدة (شدة الإضاءة)")
    with col4:
        st.subheader("المنطق: ضغط المعلومات")
        st.markdown("""
        <div class='logic-card'>
        <b>المعادلة:</b> <code>Gray = 0.299R + 0.587G + 0.114B</code> <br>
        <b>الفائدة:</b> التخلص من 66% من البيانات غير الضرورية والتركيز على تباين الإضاءة الذي يحدد شكل الحروف.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='code-window'>gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. عزل النص (Thresholding)
    st.header("🌓 3. عزل النص (Binary Thresholding)")
    st.markdown("<div class='step-box' style='border-left-color: #10b981;'>", unsafe_allow_html=True)
    col5, col6 = st.columns([1, 1.2])
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    with col5:
        st.image(thresh, use_container_width=True, caption="نص نقي (أسود وأبيض)")
    with col6:
        st.subheader("المنطق: التجريد الثنائي")
        st.markdown("""
        <div class='logic-card'>
        نستخدم خوارزمية <b>Otsu</b> لتحديد العتبة المثالية التي تفصل النص عن الخلفية. <br>
        هذا يحول الصورة إلى <span class='highlight-green'>لغة الصفر والواحد</span>، مما يجعل النص "يقفز" بوضوح للمحرك.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='code-window'>_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 4. محرك OCR
    st.header("🔍 4. محرك التعرف الضوئي (OCR Engine Deep Dive)")
    with st.spinner('جاري تشغيل الخوارزميات العصبية...'):
        reader = load_reader()  # ✅ التعديل هنا
        results = reader.readtext(image)
        
        image_with_boxes = image_rgb.copy()
        for (bbox, text, prob) in results:
            (tl, tr, br, bl) = bbox
            cv2.rectangle(image_with_boxes, (int(tl[0]), int(tl[1])), (int(br[0]), int(br[1])), (0, 255, 0), 2)
    
    st.markdown("<div class='step-box' style='border-left-color: #ec4899;'>", unsafe_allow_html=True)
    col7, col8 = st.columns([1, 1.2])
    with col7:
        st.image(image_with_boxes, use_container_width=True, caption="تحديد المواقع (Detection)")
    with col8:
        st.subheader("معمارية CRNN")
        st.markdown("""
        <div class='logic-card'>
        <b>CNN:</b> لاستخراج الميزات البصرية وتحديد مكان النص. <br>
        <b>RNN:</b> لفهم تسلسل الأحرف وعلاقتها ببعضها. <br>
        <span class='highlight-blue'>النتيجة:</span> تحويل الأشكال الهندسية إلى نصوص رقمية قابلة للتعديل.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='code-window'>results = reader.readtext(image)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    extracted_text = " ".join([res[1] for res in results])
    text_to_speak = st.text_area("النص المستخرج النهائي:", value=extracted_text, height=100)

    # 5. التفاعل البرمجي لـ TTS
    st.header("🔊 5. محاكاة التوليد الصوتي (TTS Live Coding & Animation)")
    if st.button("🚀 بدء العرض التفاعلي الختامي"):
        col_term, col_anim = st.columns([1.2, 1])
        term_placeholder = col_term.empty()
        anim_placeholder = col_anim.empty()
        
        sim_steps = [
            {"msg": "Linguistic Analysis...", "code": "from gtts import gTTS", "comment": "# تحليل النص لغوياً", "icon": "🔡"},
            {"msg": "Frequency Synthesis...", "code": "tts = gTTS(text=text, lang='ar')", "comment": "# توليد الموجات الصوتية", "icon": "🌊"},
            {"msg": "Exporting Audio...", "code": "tts.save('output.mp3')", "comment": "# حفظ النتيجة النهائية", "icon": "💾"}
        ]
        
        full_display_code = ""
        for i, step in enumerate(sim_steps):
            with anim_placeholder:
                st.markdown(f"""
                <div class='step-box' style='text-align: center;'>
                    <div style='font-size: 4rem;'>{step['icon']}</div>
                    <h3 style='color: #60a5fa;'>{step['msg']}</h3>
                    <div class='wave-container {"active-wave" if i == 1 else ""}'>
                        {"".join([f"<div class='wave-bar' style='animation-delay: {j*0.1}s'></div>" for j in range(15)])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            full_display_code += f"<div style='color: #6b7280; font-style: italic;'>{step['comment']}</div>"
            target_code = f">>> {step['code']}"
            current_line = ""
            for char in target_code:
                current_line += char
                term_placeholder.markdown(f"""
                    <div class='terminal-window'>
                        <div style='color: #888; font-size: 0.75rem; margin-bottom: 10px; border-bottom: 1px solid #222;'>LIVE CONSOLE - STEP {i+1}</div>
                        {full_display_code}
                        <div class='code-line'>{current_line}<span class='cursor'></span></div>
                    </div>
                """, unsafe_allow_html=True)
                time.sleep(0.03)
            full_display_code += f"<div class='code-line'>{target_code}</div>"
            time.sleep(1)
        
        tts = gTTS(text=text_to_speak, lang='ar')
        tts.save("output.mp3")
        st.audio("output.mp3")
        st.balloons()
else:
    st.info("💡 بانتظار رفع صورة لبدء العرض التعليمي الشامل...")