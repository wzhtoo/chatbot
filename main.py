import streamlit as st
from google import genai
from google.genai import errors

from ui import apply_chrome_hide
from config import APP_TITLE, APP_CAPTION, SYSTEM_PROMPT, MODEL

# config
st.set_page_config(page_title="Wzhtoo-AI Chat", page_icon="⚡", layout="centered")
apply_chrome_hide()

st.title(APP_TITLE)
st.caption(APP_CAPTION)

# init client
@st.cache_resource
def get_client() -> genai.Client:
    return genai.Client(api_key=st.secrets["API_KEY"])

client = get_client()

# init session state
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model=MODEL,
        config={"system_instruction": SYSTEM_PROMPT},
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# chat input
if user_input := st.chat_input("ကျွန်ုပ်အား မည်သည့်အရာမဆို မေးမြန်းနိုင်ပါသည်..."):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("WZH-Core မှ တွက်ချက်နေပါသည်..."):
            try:
                response = st.session_state.chat.send_message(user_input)
                reply = response.text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except errors.APIError as e:
                err = str(e)
                if "429" in err or "quota" in err.lower() or "rate" in err.lower():
                    st.error(
                        "🙏 တောင်းပန်ပါတယ်ခင်ဗျ။ ကျနော် free tier API သုံးထားလို့ "
                        "မြန်မာနိုင်ငံမှ billing မဖွင့်နိုင်တဲ့အတွက် ဝင်လို့မရနိုင်ပါဘူး။ "
                        "ခဏကြာမှ ပြန်လည်ကြိုးစားပေးပါ။"
                    )
                else:
                    st.error(f"⚠️ API error: {err}")

            except Exception as e:
                st.error(f"⚠️ Unexpected error: {e}")

# sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(
            model=MODEL,
            config={"system_instruction": SYSTEM_PROMPT},
        )
        st.rerun()
