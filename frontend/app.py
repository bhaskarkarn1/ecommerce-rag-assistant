import streamlit as st
import requests
import re

st.set_page_config(
    page_title="AI E-Commerce Assistant",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===========================
#        CUSTOM CSS
# ===========================
st.markdown("""
<style>
body { font-family: 'Segoe UI', sans-serif; }

.title { font-size: 42px; font-weight: 700; color: #ffffff; text-align: center; margin-bottom: 10px; }
.subtitle { font-size: 18px; color: #cccccc; text-align: center; margin-bottom: 40px; }

.stTextInput > div > div > input {
    background-color: #1e1e1e; color: white; border-radius: 10px; padding: 12px; border: 1px solid #444;
}

.stButton>button {
    background-color: #ff4b4b; color: white; padding: 12px 24px; font-size: 18px;
    border-radius: 10px; border: none; transition: 0.2s;
}
.stButton>button:hover { background-color: #e63a3a; }

.answer-box {
    background-color: #111827; padding: 25px; border-radius: 14px; border: 1px solid #333; margin-top: 20px;
}

.product-card {
    background-color: #1f2937; padding: 18px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px;
}

.product-title { font-size: 20px; font-weight: 600; color: #ffffff; }
.product-desc { font-size: 15px; color: #dddddd; }

</style>
""", unsafe_allow_html=True)


# ===========================
# CATEGORY IMAGES
# ===========================
CATEGORY_IMAGES = {
    "headphone": "https://cdn-icons-png.flaticon.com/512/1827/1827504.png",
    "earphone": "https://cdn-icons-png.flaticon.com/512/64/64572.png",
    "earbud": "https://cdn-icons-png.flaticon.com/512/64/64572.png",
    "laptop": "https://cdn-icons-png.flaticon.com/512/2422/2422118.png",
    "computer": "https://cdn-icons-png.flaticon.com/512/1998/1998767.png",
    "camera": "https://cdn-icons-png.flaticon.com/512/2920/2920235.png",
    "mobile": "https://cdn-icons-png.flaticon.com/512/15/15874.png",
    "phone": "https://cdn-icons-png.flaticon.com/512/15/15874.png",
    "speaker": "https://cdn-icons-png.flaticon.com/512/727/727245.png",
    "default": "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"
}

def detect_category(title: str):
    title_lower = title.lower()
    for key in CATEGORY_IMAGES:
        if key in title_lower:
            return key
    return "default"


# ===========================
# FRONTEND TITLE
# ===========================
st.markdown("<div class='title'>🛍️ AI E-Commerce Shopping Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Find the best products instantly using AI + Vector Search</div>", unsafe_allow_html=True)

# ===========================
# USER INPUT
# ===========================
user_query = st.text_input("🔍 Enter a product query:", placeholder="e.g., Best headphones under ₹1000")
clicked = st.button("Search")

# Initialize answer
answer = ""

# ===========================
# API CALL
# ===========================
if clicked and user_query.strip() != "":
    with st.spinner("Searching..."):
        # API CALL
        try:
            response = requests.post("http://127.0.0.1:8000/query", json={"question": user_query})
            data = response.json()
            answer = data.get("answer", "No answer returned.")
        except Exception as e:
            answer = f"❌ Error contacting backend: {e}"

    # ===========================
    # DISPLAY RESPONSE (MOVE THIS INSIDE)
    # ===========================
    st.markdown("<h3>🧠 Answer:</h3>", unsafe_allow_html=True)

    products = re.split(r"\n\s*\d+\.\s*", answer)
    products = [p.strip() for p in products if p.strip()]

    if len(products) > 1:
        for idx, product in enumerate(products, start=1):

            title_match = re.match(r"([^:–\-]+)", product)
            title = title_match.group(1).strip() if title_match else f"Product {idx}"

            category_key = detect_category(title)
            image_url = CATEGORY_IMAGES.get(category_key, CATEGORY_IMAGES["default"])

            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; gap:20px; align-items:flex-start;">
                    <img src="{image_url}"
                         style="width:140px; height:140px; border-radius:12px; 
                                object-fit:contain; background:#333; padding:10px;" />
                    <div>
                        <div class="product-title">{idx}. {title}</div>
                        <div class="product-desc">{product}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown(f"<div class='answer-box'>{answer}</div>", unsafe_allow_html=True)
