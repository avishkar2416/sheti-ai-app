import streamlit as st
from google import genai
from PIL import Image

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="स्मार्ट कृषी AI मित्र",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# २. प्रीमियम आणि मॉडर्न CSS स्टाईलिंग
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    /* मुख्य बॅकग्राउंड */
    .stApp {
        background: linear-gradient(135deg, #0d1b1e 0%, #15291e 50%, #0d1b1e 100%);
        color: #e0e6ed;
    }
    
    /* हिरवा हेडर बॅनर */
    .hero-container {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 50%, #43a047 100%);
        border-radius: 20px;
        padding: 24px 16px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        margin-bottom: 25px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .hero-title {
        color: #ffffff;
        font-size: 2.1rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .hero-subtitle {
        color: #d4edda;
        font-size: 1rem;
        margin-top: 8px;
        font-weight: 300;
    }
    
    /* मॉडर्न ग्लास कार्ड */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    /* टॅब डिझाईन */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.04);
        padding: 8px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 10px;
        color: #a0aec0;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0 18px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2e7d32, #1b5e20) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.4);
    }
    
    /* बटन्स स्टाईल */
    .stButton>button {
        background: linear-gradient(135deg, #00c853 0%, #1b5e20 100%);
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 600;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        width: 100%;
        box-shadow: 0 4px 16px rgba(0, 200, 83, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 200, 83, 0.5);
    }
    
    /* निकाल बॉक्स */
    .result-box {
        background: rgba(30, 41, 59, 0.85);
        border: 1px solid rgba(46, 125, 50, 0.4);
        border-radius: 14px;
        padding: 18px;
        margin-top: 15px;
        color: #f1f5f9;
        line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# ३. हेडर
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🌿 स्मार्ट शेती AI सहाय्यक</h1>
        <p class="hero-subtitle">अचूक पीक रोग निदान • २४/७ मराठी AI कृषी सल्लागार • खत नियोजन</p>
    </div>
""", unsafe_allow_html=True)

# API Configuration
API_KEY = "AQ.Ab8RN6JS0wf7PcFGxO3EUgVeYyvYTrU3orI9mWbw3qZfaunlrg"
MODEL_NAME = "gemini-2.5-flash"

# ४. मुख्य टॅब्स
tab1, tab2, tab3 = st.tabs(["📸 पीक रोग निदान", "💬 AI कृषी सल्लागार", "⚖️ खत गणक"])

# ----------------- TAB 1: पीक रोग निदान -----------------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🌾 पिकाच्या खराब भागाचा फोटो निवडा")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📸 अपलोड केलेले छायाचित्र", use_container_width=True)

    with col2:
        if uploaded_file:
            st.write("---")
            if st.button("✨ रोगाचे अचूक निदान करा", key="diagnose_btn"):
                with st.spinner("🤖 AI पिकाच्या रोगाचे सखोल विश्लेषण करत आहे..."):
                    try:
                        client = genai.Client(api_key=API_KEY)
                        prompt = """
                        तुम्ही एक अनुभवी कृषी शास्त्रज्ञ आहात. फोटोचे विश्लेषण करून खालील स्वरूपात स्वच्छ मराठीत माहिती द्या:
                        ### 🌾 १. पिकाचे व रोगाचे नाव
                        ### 🔍 २. रोगाची लक्षणे व कारणे
                        ### 💊 ३. जैविक आणि रासायनिक उपाय (औषधांचे नाव आणि फवारणीचे प्रमाण)
                        ### 🛡️ ४. पुढील प्रतिबंधात्मक काळजी
                        """
                        response = client.models.generate_content(
                            model=MODEL_NAME,
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
    user_query = st.text_area(
        "", 
        placeholder="उदा. सोयाबीनवर शेंगा पोखरणारी अळी आल्यास कोणती फवारणी करावी? किंवा कांदा पिकाचे वजन वाढवण्यासाठी काय करावे?",
        height=100
    )

    if st.button("🚀 तज्ज्ञ AI सल्ला मिळवा", key="ask_btn"):
        if not user_query:
            st.warning("⚠️ कृपया आधी तुमचा प्रश्न लिहा.")
        else:
            with st.spinner("🔍 कृषी माहिती शोधत आहे..."):
                try:
                    client = genai.Client(api_key=API_KEY)
                    sys_prompt = "तुम्ही महाराष्ट्रातील शेतकऱ्यांना मार्गदर्शन करणारे तज्ज्ञ कृषी शास्त्रज्ञ आहात. उत्तर नेहमी मुद्देसूद, अत्यंत सोप्या आणि शुद्ध मराठीत द्या."
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=f"{sys_prompt}\n\nशेतकऱ्याचा प्रश्न: {user_query}"
                    )
                    st.markdown(f'<div class="result-box">{response.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"एरर आला: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 3: खत नियोजन -----------------
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### ⚖️ पिकानुसार अचूक खत कॅल्क्युलेटर")
    
    c1, c2 = st.columns(2)
    with c1:
        crop = st.selectbox("🌱 पीक निवडा:", ["कापूस", "सोयाबीन", "ऊस", "कांदा", "गहू", "मका"])
    with c2:
        area = st.number_input("📐 क्षेत्रफळ (एकर मध्ये):", min_value=0.5, max_value=50.0, value=1.0, step=0.5)

    if st.button("📊 खताचे वेळापत्रक काढा"):
        st.markdown(f"#### 📋 **{crop} पिकासाठी {area} एकरचे नियोजन:**")
        if crop == "कापूस":
            st.success(f"• **युरिया:** {area * 45} ते {area * 50} किलो\n• **DAP:** {area * 50} किलो\n• **पोटॅश (MOP):** {area * 30} किलो\n• **सूक्ष्म अन्नद्रव्ये:** पाते लागताना बोरॉन व मॅग्नेशियम फवारणी.")
        elif crop == "सोयाबीन":
            st.success(f"• **DAP / 10:26:26:** {area * 50} किलो\n• **गंधक (Sulphur):** {area * 10} किलो (दाणे भरण्यासाठी अत्यंत महत्त्वाचे).")
        elif crop == "ऊस":
            st.success(f"• **युरिया:** {area * 150} किलो (३ टप्प्यांत)\n• **सिंगल सुपर फॉस्फेट (SSP):** {area * 150} किलो\n• **पोटॅश:** {area * 75} किलो.")
        else:
            st.info(f"• **{crop} मूलभूत डोस:** 10:26:26 खत {area * 50} किलो प्रति एकर वापरावे.")
    st.markdown('</div>', unsafe_allow_html=True)
