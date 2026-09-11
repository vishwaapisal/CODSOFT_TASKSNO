import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Page configuration
st.set_page_config(
    page_title="AI Image Captioning",
    page_icon="🖼️"
)

# Title
st.title("🖼️ AI Image Captioning")
st.write("Upload an image and let AI generate a caption for it.")


# Load AI model
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )

    return processor, model


# Load processor and model
processor, model = load_model()


# Image uploader
uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)


# Process uploaded image
if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        width="stretch"
    )

    # Generate caption button
    if st.button("Generate Caption"):

        with st.spinner("AI is generating the caption..."):

            inputs = processor(
                images=image,
                return_tensors="pt"
            )

            output = model.generate(
                **inputs,
                max_new_tokens=30
            )

            caption = processor.decode(
                output[0],
                skip_special_tokens=True
            )

        st.success("Caption Generated!")

        st.subheader("📝 Generated Caption")

        st.write(caption)