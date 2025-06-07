import streamlit as st
from PIL import Image
import io
import base64
import openai

# Load OpenAI key from Streamlit secrets
openai.api_key = st.secrets["openai_key"]

# App UI
st.set_page_config(page_title="MediScan AI", layout="centered")
st.title("📸 MediScan AI - Medication Label Reader")
st.write("Upload a photo of your medication label and let AI extract details like name, dosage, and intake time.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Read image bytes
    image_bytes = uploaded_file.read()

    # Load and resize image
    image = Image.open(io.BytesIO(image_bytes))
    image = image.convert("RGB")
    image = image.resize((600, 400))  # Resize to reduce token usage

    # Show the resized image
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Encode resized image to base64
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    resized_image_bytes = buffer.getvalue()
    base64_image = base64.b64encode(resized_image_bytes).decode("utf-8")
    data_url = f"data:image/jpeg;base64,{base64_image}"

    # GPT-4o Vision request
    try:
        client = openai.OpenAI()
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
        st.success("✅ Extracted Information:")
        st.write(result)

    except Exception as e:
        st.error(f"❌ AI Error: {str(e)}")
