import streamlit as st
import openai
from PIL import Image
import base64
import io

# Load your OpenAI API key securely from Streamlit secrets
openai.api_key = st.secrets["openai_key"]

st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("🧠 MediScan AI - Medication Label Reader")
st.write("Upload a photo of your medication label and let AI extract details like name, dosage, and intake time.")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Read image bytes
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_bytes = buffered.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:image/png;base64,{base64_image}"

    st.spinner("Analyzing...")

    # Use OpenAI GPT-4o to extract medication details
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts medication name, dosage, and intake time from images."},
                {"role": "user", "content": data_url}
            ]
        )

        result = response.choices[0].message.content
        st.success("Extraction Successful!")
        st.markdown(result)

    except openai.OpenAIError as e:
        st.error(f"AI Error: {e}")
