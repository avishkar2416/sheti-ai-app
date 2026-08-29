import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(
    page_title="स्मार्ट कृषी AI मित्र",
    page_icon="🌿",
    layout="wide"
)

# मॉडर्न स्टाईल
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
    .stApp { background: linear-gradient(135deg, #0d1b1e 0%, #15291e 50%, #0d1b1e 100%); color: #e0e6ed; }
    .hero-container {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #43a047 100%);
        border-radius: 20px; padding: 22px 15px; text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4); margin-bottom: 25px;
    }
    .hero-title { color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0; }
    .hero-subtitle { color: #d4edda; font-size: 0.95rem; margin-top: 6px; }
    .glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00c853 0%, #1b5e20 100%);
        color: #ffffff; font-size: 1.05rem; font-weight: 600; border-radius: 12px;
        border: none; padding: 12px 24px; width: 100%; box-shadow: 0 4px 16px rgba(0, 200, 83, 0.3);
    }
    .result-box {
        background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(46, 125, 50, 0.4);
        border-radius: 14px; padding: 18px; margin-top: 15px; color: #f1f5f9; line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🌿 स्मार्ट शेती AI सहाय्यक</h1>
        <p class="hero-subtitle">अचूक पीक रोग निदान • २४/७ मराठी AI कृषी सल्लागार • खत नियोजन</p>
    </div>
""", unsafe_allow_html=True)

# स्क्रीनवर थेट दिसणारा API Key बॉक्स
api_key = st.text_input("🔑 तुमची Gemini API Key येथे पेस्ट करा:", type="password", value="AQ.Ab8RN6L7fDObKeEHsrh31oDazDR2ZTfP5uG2KgNwG7JheupVNA")

tab1, tab2, tab3 = st.tabs(["📸 पीक रोग निदान", "💬 AI कृषी सल्लागार", "⚖️ खत गणक"])

# ----------------- TAB 1: पीक रोग निदान -----------------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🌾 पिकाच्या खराब भागाचा फोटो निवडा")
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 अपलोड केलेले छायाचित्र", use_container_width=True)
        
        if st.button("✨ रोगाचे अचूक निदान करा", key="diagnose_btn"):
            if not api_key:
                st.error("कृपया आधी API Key टाका.")
            else:
                with st.spinner("🤖 AI पिकाच्या रोगाचे सखोल विश्लेषण करत आहे..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = """
                        तुम्ही एक अनुभवी कृषी शास्त्रज्ञ आहात. फोटोचे विश्लेषण करून खालील स्वरूपात स्वच्छ मराठीत माहिती द्या:
                        1. पिकाचे व रोगाचे नाव
                        2. रोगाची मुख्य लक्षणे व कारणे
                        3. जैविक आणि रासायनिक उपाय (औषधांचे नाव आणि फवारणीचे प्रमाण)
                        4. पुढील प्रतिबंधात्मक काळजी
                        """
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[image, prompt]
                        )
                        st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"एरर आला: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 2: AI कृषी सल्लागार -----------------
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 💬 शेतीविषयक काहीही विचारा")
    user_query = st.text_area("", placeholder="उदा. सोयाबीनवर कोणती कीटकनाशक फवारणी करावी?")

    if st.button("🚀 तज्ज्ञ AI सल्ला मिळवा", key="ask_btn"):
        if not api_key:
            st.error("कृपया आधी API Key टाका.")
        elif not user_query:
            st.warning("कृपया आधी प्रश्न लिहा.")
        else:
            with st.spinner("🔍 माहिती शोधत आहे..."):
                try:
                    client = genai.Client(api_key=api_key)
                    sys_prompt = "तुम्ही तज्ज्ञ कृषी अधिकारी आहात. उत्तर शुद्ध व सोप्या मराठीत द्या."
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{sys_prompt}\n\nप्रश्न: {user_query}"
                    )
                    st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"एरर आला: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 3: खत नियोजन -----------------
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### ⚖️ पिकानुसार अचूक खत कॅल्क्युलेटर")
    crop = st.selectbox("🌱 पीक निवडा:", ["कापूस", "सोयाबीन", "ऊस", "कांदा", "गहू", "मका"])
    area = st.number_input("📐 क्षेत्रफळ (एकर):", min_value=0.5, max_value=50.0, value=1.0, step=0.5)

    if st.button("📊 खताचे वेळापत्रक काढा"):
        if crop == "कापूस":
            st.success(f"• **युरिया:** {area * 50} किलो\n• **DAP:** {area * 50} किलो\n• **पोटॅश:** {area * 30} किलो")
        elif crop == "सोयाबीन":
            st.success(f"• **DAP / 10:26:26:** {area * 50} किलो\n• **गंधक (Sulphur):** {area * 10} किलो")
        elif crop == "ऊस":
            st.success(f"• **युरिया:** {area * 150} किलो\n• **SSP:** {area * 150} किलो\n• **पोटॅश:** {area * 75} किलो")
        else:
            st.info(f"• **{crop} डोस:** 10:26:26 खत {area * 50} किलो प्रति एकर.")
    st.markdown('</div>', unsafe_allow_html=True)
