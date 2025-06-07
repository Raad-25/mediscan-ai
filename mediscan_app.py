import streamlit as st
import base64
from PIL import Image
from openai import OpenAI

# Load API key securely from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai_key"])

st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("🧠 MediScan AI - Medication Label Reader")
st.write("Upload a photo of your medication label and let AI extract details like name, dosage, and intake time.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Read image bytes once
    image = Image.open(uploaded_file)
    image_bytes = uploaded_file.read()
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Encode to base64 for GPT-4o
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{base64_image}"

    # Send to OpenAI
    with st.spinner("Analyzing..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a medical assistant that extracts name, dosage, and intake time from medication label images."},
                {"role": "user", "content": [{"type": "image_url", "image_url": {"url": data_url}}]}
            ]
        )

        output = response.choices[0].message.content
        st.markdown("### 📝 Extracted Information")
        st.write(output)
