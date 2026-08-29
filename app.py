import streamlit as st
from google import genai
from PIL import Image

# पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="स्मार्ट शेतकरी AI मित्र",
    page_icon="🌱",
    layout="wide"
)

# स्टाईलिंग
st.markdown("""
    <style>
    .main-title {
        color: #2e7d32;
        text-align: center;
        font-size: 2.3rem;
        font-weight: bold;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# हेडर
st.markdown("<div class='main-title'>🌱 स्मार्ट शेती AI सहाय्यक</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>पिकांचे रोग निदान, खत नियोजन आणि मराठीतून AI शेती सल्ला</div>", unsafe_allow_html=True)

# Sidebar - API Key आणि सेटिंग्ज
with st.sidebar:
    st.header("⚙️ सेटिंग्स")
    api_key = st.text_input("तुमची Gemini API Key टाका:", type="password")
    st.markdown("---")
    st.write("💡 **टीप:** मोफत API Key मिळवण्यासाठी [Google AI Studio](https://aistudio.google.com/) ला भेट द्या.")

# मुख्य टॅब्स
tab1, tab2, tab3 = st.tabs(["📸 पीक रोग निदान (Crop Doctor)", "💬 शेती AI सल्लागार", "⚖️ खत नियोजन"])

# ----------------- TAB 1: पीक रोग निदान -----------------
with tab1:
    st.subheader("पानाचा/पिकाचा फोटो अपलोड करा")
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader("पिकाच्या खराब भागाचा फोटो निवडा:", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="अपलोड केलेला फोटो", use_container_width=True)

    with col2:
        if uploaded_file is not None:
            if st.button("🔍 रोगाचे निदान करा", type="primary"):
                if not api_key:
                    st.error("कृपया डाव्या बाजूला तुमची Gemini API Key टाका.")
                else:
                    with st.spinner("AI पिकाच्या रोगाचे विश्लेषण करत आहे..."):
                        try:
                            client = genai.Client(api_key=api_key)
                            prompt = """
                            तुम्ही एक अनुभवी कृषी शास्त्रज्ञ आहात. दिलेल्या पिकाच्या किंवा वनस्पतीच्या फोटोचे काळजीपूर्वक विश्लेषण करा आणि खालील मुद्द्यांमध्ये सोप्या मराठी भाषेत माहिती द्या:
                            1. पिकाचे नाव व रोगाचे नाव (Identify Crop & Disease)
                            2. रोगाची मुख्य लक्षणे आणि कारणे (Symptoms & Causes)
                            3. जैविक व रासायनिक उपाय (खते व औषधांची नावे आणि फवारणीचे प्रमाण)
                            4. भविष्यात रोग टाळण्यासाठी घ्यायची काळजी
                            """
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=[image, prompt]
                            )
                            st.success("विश्लेषण पूर्ण झाले!")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"एरर आला: {e}")

# ----------------- TAB 2: शेती AI सल्लागार -----------------
with tab2:
    st.subheader("शेतीविषयक कोणताही प्रश्न विचारा")
    user_query = st.text_area("तुमचा प्रश्न येथे लिहा (उदा. कापूस पिकावर बोंडअळी आल्यास काय करावे?):")

    if st.button("🤖 सल्ला मिळवा", type="primary"):
        if not api_key:
            st.error("कृपया डाव्या बाजूला तुमची Gemini API Key टाका.")
        elif not user_query:
            st.warning("कृपया आधी तुमचा प्रश्न लिहा.")
        else:
            with st.spinner("माहिती शोधत आहे..."):
                try:
                    client = genai.Client(api_key=api_key)
                    sys_prompt = "तुम्ही महाराष्ट्रातील शेतकऱ्यांना मार्गदर्शन करणारे तज्ज्ञ कृषी अधिकारी आहात. उत्तर नेहमी शुद्ध, सोप्या आणि मुद्देसूद मराठीत द्या."
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=f"{sys_prompt}\n\nशेतकऱ्याचा प्रश्न: {user_query}"
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"एरर आला: {e}")

# ----------------- TAB 3: खत नियोजन -----------------
with tab3:
    st.subheader("पिकानुसार खत प्रमाण कॅल्क्युलेटर")
    crop = st.selectbox("पीक निवडा:", ["कापूस", "सोयाबीन", "ऊस", "कांदा", "गहू", "मका"])
    area = st.number_input("क्षेत्रफळ (एकर मध्ये):", min_value=0.5, max_value=50.0, value=1.0, step=0.5)

    if st.button("📊 खताचे नियोजन दाखवा"):
        st.write(f"### {crop} पिकासाठी {area} एकरचे अंदाजे खत नियोजन:")
        if crop == "कापूस":
            st.info(f"• युरिया: {area * 45} ते {area * 50} किलो\n• DAP: {area * 50} किलो\n• MOP (पोटॅश): {area * 30} किलो\n• सूक्ष्म अन्नद्रव्ये: आवश्यकतेनुसार फवारणी.")
        elif crop == "सोयाबीन":
            st.info(f"• DAP / 10:26:26: {area * 50} किलो\n• गंधक (Sulphur): {area * 10} किलो (पेरणीच्या वेळी).")
        elif crop == "ऊस":
            st.info(f"• युरिया: {area * 150} किलो (३-४ टप्प्यांत)\n• सिंगल सुपर फॉस्फेट (SSP): {area * 150} किलो\n• पोटॅश: {area * 75} किलो.")
        else:
            st.info(f"• {crop} पिकासाठी मूलभूत डोस: 10:26:26 किंवा 20:20:0:13 खत {area * 50} किलो प्रति एकर वापरावे.")
