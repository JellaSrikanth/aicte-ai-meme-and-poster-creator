# 🎨 AI Meme & Poster Creator

This is a simple web application built with Streamlit that allows users to generate memes and posters. The app uses the Stable Diffusion model via the Hugging Face API to create an image based on a user's text description. It then overlays a user-provided caption onto the image.

## Features

-   Generate images from text prompts.
-   Add custom text captions to the images.
-   Simple, easy-to-use web interface.
-   Download the final generated image.

## Setup and Installation

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)

### Steps

1.  **Download the Files:**
    Save the `app.py`, `requirements.txt`, and `README.md` files into a new folder on your computer.

2.  **Install Dependencies:**
    Open a terminal or command prompt, navigate to the project folder, and run the following command to install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This application requires a **Hugging Face API Token** to generate images.

1.  **Get a Token:** Go to [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) to get your free API token. You will need to sign up for an account.
2.  **Use the Token:** When you run the application, a sidebar will appear. Paste your API token into the "Hugging Face API Token" input box.

## How to Run the Application

1.  Make sure you are in the project folder in your terminal.
2.  Run the following command:
    ```bash
    streamlit run app.py
    ```
3.  The application will open automatically in your web browser.