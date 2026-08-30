import streamlit as st
from google import genai
from PIL import Image
import requests
import pandas as pd

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="स्मार्ट कृषी AI मित्र",
    page_icon="🌾",
    layout="wide"
)

# २. प्रीमियम स्टाईलिंग
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
    .hero-title { color: #ffffff; font-size: 2.1rem; font-weight: 700; margin: 0; }
    .hero-subtitle { color: #d4edda; font-size: 1rem; margin-top: 6px; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 16px; padding: 20px; margin-bottom: 20px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px; background: rgba(255, 255, 255, 0.04);
        padding: 8px; border-radius: 14px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px; border-radius: 10px; color: #a0aec0; font-weight: 600; font-size: 0.95rem;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2e7d32, #1b5e20) !important;
        color: #ffffff !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #00c853 0%, #1b5e20 100%);
        color: #ffffff; font-size: 1.05rem; font-weight: 600; border-radius: 12px;
        border: none; padding: 12px 24px; width: 100%; box-shadow: 0 4px 16px rgba(0, 200, 83, 0.3);
    }
    
    .result-box {
        background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(46, 125, 50, 0.5);
        border-radius: 14px; padding: 18px; margin-top: 15px; color: #f1f5f9; line-height: 1.7;
    }
    </style>
""", unsafe_allow_html=True)

# हेडर बॅनर
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🌾 स्मार्ट शेतकरी AI महा-पोर्टल</h1>
        <p class="hero-subtitle">रोग निदान • थेट जिल्हावार APMC बाजारभाव • खत व हवामान सल्ला</p>
    </div>
""", unsafe_allow_html=True)

# Secrets मधून की लोड करणे
api_key = st.secrets.get("GEMINI_API_KEY", "")

# AI कॉल फंक्शन
def generate_ai_response(client, contents):
    models = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
    for m in models:
        try:
            res = client.models.generate_content(
                model=m,
                contents=contents
            )
            return res.text
        except Exception:
            continue
    raise Exception("मॉडेल लोड होऊ शकले नाही. कृपया API Key तपासा.")

# ५ मुख्य टॅब्स
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📸 पीक डॉक्टर (रोग निदान)", 
    "📈 थेट जिल्हावार APMC बाजारभाव",
    "💬 AI शेती सल्लागार", 
    "⚖️ खत व फवारणी खर्च", 
    "🌦️ फवारणी हवामान अलर्ट"
])

# ----------------- TAB 1: पीक डॉक्टर -----------------
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🌾 पिकाच्या खराब भागाचा फोटो निवडा")
    
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📸 शेतातील फोटो", use_container_width=True)
        
        if st.button("✨ रोगाचे सखोल निदान व खर्च काढा", key="diagnose_btn"):
            if not api_key:
                st.error("कृपया Streamlit Secrets मध्ये API Key जोडा.")
            else:
                with st.spinner("🤖 AI पिकाचे विश्लेषण व उपाय शोधत आहे..."):
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = """
                        तुम्ही एक अनुभवी वरिष्ठ कृषी शास्त्रज्ञ आहात. पिकाच्या फोटोचे काळजीपूर्वक विश्लेषण करून खालील स्वरूपात स्वच्छ व सोप्या मराठीत माहिती द्या:
                        ### 🌾 १. पिकाचे नाव व रोगाचे अचूक नाव (Disease Diagnosis)
                        ### 🔍 २. मुख्य लक्षणे व रोग पडण्याचे कारण (Symptoms & Causes)
                        ### 💊 ३. शिफारस केलेली औषधे व फवारणीचे प्रमाण (प्रति १५ लिटर पंप आणि प्रति एकर)
                        ### 💰 ४. अंदाजे औषधांचा एकरी खर्च (Estimated Cost per Acre)
                        ### 🛡️ ५. पुढील प्रतिबंधात्मक काळजी (Prevention Tips)
                        """
                        result = generate_ai_response(client, [image, prompt])
                        st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"एरर आला: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 2: थेट जिल्हावार APMC बाजारभाव -----------------
with tab4 if False else tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🏛️ महाराष्ट्र कृषी उत्पन्न बाजार समिती (APMC) थेट चालू दर")
    st.caption("स्रोत: भारत सरकार कृषी व शेतकरी कल्याण मंत्रालय (Agmarknet Live API)")
    
    # महाराष्ट्रातील सर्व ३६ जिल्हे
    mh_districts = [
        "सर्व जिल्हे", "Ahmednagar", "Akola", "Amravati", "Beed", "Bhandara", "Buldhana", 
        "Chandrapur", "Chhatrapati Sambhajinagar", "Dhule", "Gadchiroli", "Gondia", 
        "Hingoli", "Jalgaon", "Jalna", "Kolhapur", "Latur", "Nagpur", "Nanded", 
        "Nandurbar", "Nashik", "Dharashiv", "Palghar", "Parbhani", "Pune", 
        "Raigad", "Ratnagiri", "Sangli", "Satara", "Sindhudurg", "Solapur", 
        "Thane", "Wardha", "Washim", "Yavatmal"
    ]
    
    # प्रमुख पिके
    commodity_list = [
        "Soyabean", "Cotton", "Onion", "Gram(Chana)", "Arhar (Tur/Red Gram)", 
        "Wheat", "Maize", "Paddy(Dhan)", "Tomato", "Potato", "Green Chilli", "Ginger"
    ]
    
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        selected_district = st.selectbox("📍 तुमचा जिल्हा निवडा:", mh_districts)
    with c_m2:
        selected_commodity = st.selectbox("🌱 पीक/शेतमाल निवडा:", commodity_list)
        
    if st.button("🔍 थेट चालू बाजारभाव शोधा", key="mandi_fetch_btn"):
        with st.spinner("कृषी विभागाच्या सर्व्हरवरून थेट चालू बाजारभाव लोड करत आहे..."):
            try:
                # Government Agmarknet API Endpoint
                api_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
                params = {
                    "api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
                    "format": "json",
                    "offset": "0",
                    "limit": "100",
                    "filters[state]": "Maharashtra",
                    "filters[commodity]": selected_commodity
                }
                
                if selected_district != "सर्व जिल्हे":
                    params["filters[district]"] = selected_district
                    
                res = requests.get(api_url, params=params, timeout=12)
                data = res.json()
                
                if "records" in data and len(data["records"]) > 0:
                    records = data["records"]
                    formatted_data = []
                    for r in records:
                        formatted_data.append({
                            "तारीख": r.get("arrival_date", "-"),
                            "जिल्हा": r.get("district", "-"),
                            "बाजार समिती (APMC)": r.get("market", "-"),
                            "शेतमाल / जात": f"{r.get('commodity', '')} ({r.get('variety', '-')})",
                            "किमान भाव (₹/क्विंटल)": f"₹{r.get('min_price', '-')}",
                            "कमाल भाव (₹/क्विंटल)": f"₹{r.get('max_price', '-')}",
                            "सरासरी भाव (₹/क्विंटल)": f"₹{r.get('modal_price', '-')}"
                        })
                    
                    df = pd.DataFrame(formatted_data)
                    st.success(f"✅ {selected_district} मधील {selected_commodity} चे चालू बाजारभाव:")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.warning(f"⚠️ {selected_district} बाजार समितीत आज {selected_commodity} ची आवक नोंद झालेली नाही किंवा सौदे अद्याप सुरू आहेत.")
            except Exception as e:
                st.error("सर्व्हरवरून थेट डेटा आणण्यात अडचण आली. कृपया काही वेळाने पुन्हा प्रयत्न करा.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 3: AI शेती सल्लागार -----------------
with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 💬 शेतीतील कोणताही प्रश्न मराठीत विचारा")
    user_query = st.text_area("", placeholder="उदा. सोयाबीन ४० दिवसांचे आहे, फुलगळ थांबवण्यासाठी आणि शेंगांची संख्या वाढवण्यासाठी कोणती फवारणी करू?")

    if st.button("🚀 तज्ज्ञ कृषी सल्ला मिळवा", key="ask_btn"):
        if not api_key:
            st.error("कृपया Streamlit Secrets मध्ये API Key जोडा.")
        elif not user_query:
            st.warning("⚠️ कृपया आधी प्रश्न लिहा.")
        else:
            with st.spinner("🔍 कृषी विद्यापीठाच्या शिफारशी शोधत आहे..."):
                try:
                    client = genai.Client(api_key=api_key)
                    sys_prompt = "तुम्ही महाराष्ट्रातील शेतकऱ्यांना मार्गदर्शन करणारे तज्ज्ञ कृषी अधिकारी आहात. उत्तर नेहमी अत्यंत सोपे, मुद्देसूद, औषधांची अचूक नावे आणि प्रमाणासह मराठीत द्या."
                    result = generate_ai_response(client, f"{sys_prompt}\n\nशेतकऱ्याचा प्रश्न: {user_query}")
                    st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"एरर आला: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 4: खत व फवारणी खर्च -----------------
with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### ⚖️ पिकानुसार एकरी खत व अंदाजे खर्च नियोजन")
    c1, c2 = st.columns(2)
    with c1:
        crop = st.selectbox("🌱 पीक निवडा:", ["सोयाबीन", "कापूस", "ऊस", "कांदा", "तूर", "गहू", "मका"])
    with c2:
        area = st.number_input("📐 क्षेत्रफळ (एकर):", min_value=0.5, max_value=50.0, value=1.0, step=0.5)

    if st.button("📊 संपूर्ण खत वेळापत्रक व खर्च दाखवा"):
        st.markdown(f"#### 📋 **{crop} पिकासाठी {area} एकरचे खत वेळापत्रक:**")
        if crop == "सोयाबीन":
            st.success(f"""
            • **पेरणीवेळी खत:** 10:26:26 किंवा 20:20:0:13 = {int(area * 50)} किलो + सल्फर (गंधक) {int(area * 10)} किलो.
            • **पहिली फवारणी (२५ दिवस):** 19:19:19 खत (७५ ग्रॅम/पंप) + अळीनाशक.
            • **दुसरी फवारणी (फुलोऱ्यात):** 12:61:00 किंवा 0:52:34 (७५ ग्रॅम/पंप) + बोरॉन (२० ग्रॅम).
            • **अंदाजे एकरी खर्च:** ₹२,५०० ते ₹३,२०० प्रति एकर.
            """)
        elif crop == "कापूस":
            st.success(f"""
            • **बेसल डोस (लागवड):** DAP {int(area * 50)} किलो + पोटॅश {int(area * 30)} किलो.
            • **पहिले खत (३० दिवस):** युरिया {int(area * 35)} किलो + 10:26:26 {int(area * 50)} किलो.
            • **पाते लागताना:** बोरॉन फवारणी + 0:52:34 खत.
            • **अंदाजे एकरी खर्च:** ₹३,८०० ते ₹४,५०० प्रति एकर.
            """)
        elif crop == "ऊस":
            st.success(f"""
            • **लागवड डोस:** Single Super Phosphate (SSP) {int(area * 150)} किलो + युरिया {int(area * 50)} किलो.
            • **बाळ बांधणी (६० दिवस):** 10:26:26 {int(area * 100)} किलो + युरिया {int(area * 50)} किलो.
            • **मोठी बांधणी:** पोटॅश {int(area * 75)} किलो + युरिया {int(area * 100)} किलो.
            • **अंदाजे एकरी खर्च:** ₹७,००० ते ₹९,००० प्रति एकर.
            """)
        else:
            st.info(f"• **{crop} मूलभूत नियोजन:** 10:26:26 खत {int(area * 50)} किलो प्रति एकर वापरावे. अंदाजे खर्च: ₹२,२०० प्रति एकर.")
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 5: फवारणी हवामान अलर्ट -----------------
with tab5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.write("### 🌦️ फवारणीसाठी आजचे हवामान कसे आहे?")
    
    weather_col1, weather_col2 = st.columns(2)
    with weather_col1:
        time_slot = st.selectbox("फवारणीची वेळ निवडा:", ["सकाळी (७ ते ११)", "दुपारी (१२ ते ३)", "संध्याकाळी (४ ते ७)"])
        wind = st.selectbox("वाऱ्याचा वेग कसा आहे?", ["मंद हवा / शांत", "मध्यम वारा", "खूप जोराचा वारा"])
    
    with weather_col2:
        sky = st.selectbox("आकाशात ढग आहेत का?", ["निरभ्र ऊन आहे", "हलके ढग आहेत", "काळवंडलेले ढग / पावसाची शक्यता"])
        
    if st.button("🛡️ फवारणी करावी की नाही ते तपासा"):
        if sky == "काळवंडलेले ढग / पावसाची शक्यता":
            st.error("⛔ **सल्ला:** फवारणी अजिबात करू नका! पाऊस आल्यास औषध वाहून जाऊन पैशांचे मोठे नुकसान होईल.")
        elif wind == "खूप जोराचा वारा":
            st.warning("⚠️ **सल्ला:** जोरदार वाऱ्यात फवारणी टाळा. औषध उडून हवेत जाईल आणि झाडावर बसणार नाही.")
        elif time_slot == "दुपारी (१२ ते ३)":
            st.warning("⚠️ **सल्ला:** कडक उन्हात फवारणी करू नका. औषधाची वाफ होते आणि पानांना झटका बसू शकतो.")
        else:
            st.success("✅ **उत्तम वेळ!** फवारणीसाठी हवामान अनुकूल आहे. औषधात स्टिकर (Silicon Spreader) नक्की वापरावे.")
    st.markdown('</div>', unsafe_allow_html=True)
