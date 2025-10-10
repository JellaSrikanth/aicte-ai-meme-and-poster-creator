import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# MODIFIED: API URL for Unsplash
API_URL = "https://api.unsplash.com/search/photos"

# --- Helper Functions ---

def fetch_unsplash_image(api_key, query):
    """Searches Unsplash for an image and returns it."""
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data["results"]:
            image_url = data["results"][0]["urls"]["regular"]
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image = Image.open(BytesIO(image_response.content))
            return image
        else:
            st.error(f"No images found on Unsplash for '{query}'. Please try another search term.")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error calling the Unsplash API: {e}")
        return None

def add_text_to_image(image, text):
    """Adds a caption to the top of the image."""
    if not text:
        return image
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default(size=50) # Increased font size
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    
    image_width, image_height = image.size
    position = ((image_width - text_width) / 2, 20) # Moved text down a bit

    draw.text(position, text, font=font, fill="white", stroke_width=2, stroke_fill="black")
    return image

# --- Streamlit App UI ---

# MODIFIED: Updated title
st.set_page_config(layout="wide", page_title="Image Finder & Meme Creator")
st.title("🖼️ Image Finder & Meme Creator")
st.markdown("Find a high-quality photo from Unsplash and add your own caption.")

# --- Sidebar ---
with st.sidebar:
    st.header("Configuration")
    st.success("✅ API Key Loaded Securely")
    st.info("This app connects to the Unsplash API using a secure backend key.")
    
    # MODIFIED: Securely get the Unsplash API Key from Streamlit Secrets
    unsplash_key = st.secrets["UNSPLASH_KEY"]

# --- Main Content ---
col1, col2 = st.columns(2)

with col1:
    # MODIFIED: Changed prompt to be a search query
    st.subheader("Step 1: Search for an Image")
    image_prompt = st.text_area(
        "What kind of photo are you looking for?", 
        "astronaut riding a horse",
        height=100
    )

    st.subheader("Step 2: Add Your Caption")
    text_overlay = st.text_input(
        "What text should appear on the image?", 
        "Just another Tuesday."
    )

    if st.button("✨ Create Meme!", type="primary"):
        if not unsplash_key:
            st.error("Unsplash API Key is not configured in the secrets.")
        elif not image_prompt:
            st.warning("Please enter a search term for the image.")
        else:
            with st.spinner("Finding the perfect photo on Unsplash..."):
                # MODIFIED: Call the new function
                found_image = fetch_unsplash_image(unsplash_key, image_prompt)
                
                if found_image:
                    final_image = add_text_to_image(found_image, text_overlay)
                    st.session_state.final_image = final_image
                    st.success("Done!")

with col2:
    st.subheader("Result")
    if 'final_image' in st.session_state:
        st.image(st.session_state.final_image, caption="Your final image", use_container_width=True)
        
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
        st.info("Your image will appear here.")