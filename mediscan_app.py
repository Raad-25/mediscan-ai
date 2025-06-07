import streamlit as st
import openai
from PIL import Image
import base64

# Securely load your OpenAI key from Streamlit secrets
openai.api_key = st.secrets["openai_key"]

st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("📸 MediScan AI - Medication Label Reader")
st.write("Upload a photo of your medication label and let AI extract details like name, dosage, and intake time.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Read image bytes once
    image_bytes = uploaded_file.read()

    # Show the image in the UI
    st.image(image_bytes, caption="Uploaded Image", use_container_width=True)

    # Convert to base64 string
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{base64_image}"

    with st.spinner("Analyzing with GPT-4o..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract the medication name, dosage, and intake time from this label image. Format the result as a clean table."},
                            {"type": "image_url", "image_url": {"url": data_url}},
                        ],
                    }
                ],
                max_tokens=500
            )
            result = response["choices"][0]["message"]["content"]
            st.markdown(result)
        except Exception as e:
            st.error(f"❌ AI Error: {e}")
