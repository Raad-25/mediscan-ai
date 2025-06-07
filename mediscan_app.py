import streamlit as st
import openai
from PIL import Image
import base64

# Load API key securely from Streamlit secrets
openai.api_key = st.secrets["openai_key"]

# Configure Streamlit page
st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("📸 MediScan AI - Medication Label Reader")
st.write("Upload a photo of your medication label and let AI extract details like name, dosage, and intake time.")

# Image uploader
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Read and display image
    image_bytes = uploaded_file.read()
    st.image(image_bytes, caption="Uploaded Image", use_container_width=True)

    # Encode image in base64 for GPT-4o
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{base64_image}"

    # Call OpenAI GPT-4o with vision capability
    try:
        client = openai.OpenAI(api_key=openai.api_key)  # ✅ Explicitly pass the key here

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract medication name, dosage, and intake time from this label:"},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ],
                }
            ],
            max_tokens=500
        )

        result = response.choices[0].message.content
        st.subheader("🧾 Extracted Information")
        st.write(result)

    except Exception as e:
        st.error(f"❌ AI Error: {e}")
