import streamlit as st
import openai
from PIL import Image
import base64
import io

# Securely load your OpenAI key from Streamlit secrets
openai.api_key = st.secrets["openai_key"]

# App UI
st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("🩺 MediScan AI - Medication Label Reader")
st.write("Upload a photo of your medication label and let AI extract details like name, dosage, and intake time.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Read image bytes once
    image_bytes = uploaded_file.read()

    # Show the image
    st.image(image_bytes, caption="Uploaded Image", use_container_width=True)

    # Encode to base64 for GPT-4o
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{base64_image}"

    # GPT-4o call
    try:
        client = openai.OpenAI(api_key=openai.api_key)  # ✅ Explicitly pass the API key here
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts medication name, dosage, and intake time from images."},
                {"role": "user", "content": data_url}
            ]
        )

        result = response.choices[0].message.content.strip()
        st.markdown("### Extracted Information")
        st.write(result)

    except Exception as e:
        st.error(f"AI Error: {str(e)}")
