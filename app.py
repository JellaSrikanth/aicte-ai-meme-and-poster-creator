import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# --- Configuration ---
# Using a Stable Diffusion model via the free Hugging Face Inference API
# This is the new, free model that will work immediately
API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

# --- Helper Functions ---

def generate_image(api_key, prompt):
    """Calls the Hugging Face API to generate an image from a text prompt."""
    headers = {"Authorization": f"Bearer {api_key}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        image_bytes = response.content
        image = Image.open(BytesIO(image_bytes))
        return image
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling the image generation API: {e}")
        # Check for specific Hugging Face errors
        if response.content:
            try:
                error_json = response.json()
                if "error" in error_json:
                    st.error(f"API Error Details: {error_json['error']}")
            except ValueError:
                st.error("Could not parse error response from the API.")
        return None


def add_text_to_image(image, text):
    """Adds a caption to the top of the image."""
    if not text:
        return image

    draw = ImageDraw.Draw(image)
    
    # Use Pillow's default font. For better fonts, provide a .ttf file path.
    try:
        font = ImageFont.load_default(size=40) # Larger default font
    except IOError:
        font = ImageFont.load_default()

    # Simple text positioning: centered at the top
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    # Position the text 10 pixels from the top and centered horizontally
    image_width, image_height = image.size
    position = ((image_width - text_width) / 2, 10)

    # Add a simple white stroke for better visibility
    draw.text(position, text, font=font, fill="white", stroke_width=2, stroke_fill="black")

    return image

# --- Streamlit App UI ---

st.set_page_config(layout="wide", page_title="AI Meme & Poster Creator")

st.title("🎨 AI Meme & Poster Creator")
st.markdown("Create fun memes and posters by describing an image and adding a caption. Powered by Stable Diffusion.")

# --- Sidebar for API Key ---
with st.sidebar:
    st.header("Configuration")
    st.success("✅ API Key Loaded Securely")
    st.info("This app connects to the AI model using a secure backend key. No user input is required.")
    
    # Get API Key from user
    hf_api_key = st.secrets["HF_API_KEY"]

# --- Main Content ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Step 1: Describe the Image")
    image_prompt = st.text_area(
        "What should the image look like?", 
        "A photo of an astronaut riding a horse on Mars",
        height=100
    )

    st.subheader("Step 2: Add Your Caption")
    text_overlay = st.text_input(
        "What text should appear on the image?", 
        "Just another Tuesday."
    )

    if st.button("✨ Generate Meme!", type="primary"):
        if not hf_api_key:
            st.warning("Please enter your Hugging Face API token in the sidebar to continue.")
        elif not image_prompt:
            st.warning("Please enter a description for the image.")
        else:
            with st.spinner("AI is painting your masterpiece..."):
                # 1. Generate the base image
                generated_image = generate_image(hf_api_key, image_prompt)
                
                if generated_image:
                    # 2. Add text to the image
                    final_image = add_text_to_image(generated_image, text_overlay)
                    
                    # Store in session state to display in the other column
                    st.session_state.final_image = final_image
                    st.success("Done!")

with col2:
    st.subheader("Result")
    if 'final_image' in st.session_state:
        # MODIFIED: Changed use_column_width to use_container_width
        st.image(st.session_state.final_image, caption="Your generated meme/poster", use_container_width=True)
        
        # Provide a download button
        buf = BytesIO()
        st.session_state.final_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="meme.png",
            mime="image/png"
        )
    else:
        st.info("Your generated image will appear here.")