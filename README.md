# 🖼️ Image Finder & Meme Creator

This is a web application built with Streamlit that allows users to find high-quality, royalty-free photos from Unsplash and add a custom text caption to create a meme or poster.

## Features

* **Image Search**: Finds real, high-quality photos using the Unsplash API based on a text query.
* **Text Overlay**: Adds custom text captions on top of the found images.
* **Secure API Management**: Uses Streamlit's built-in Secrets Management for safe handling of the Unsplash API key.
* **Download Functionality**: Allows users to download their final creation as a PNG file.

## Configuration & Security 🔑

This application is designed to be deployed on **Streamlit Community Cloud** and uses its **Secrets Management** to securely handle the Unsplash Access Key.

The API key is stored as a secure environment variable on the server and is loaded in the backend using `st.secrets`. It is never exposed in the source code or to the end-user.

## How to Run the Application

This app is intended to be run from the live deployment link on Streamlit Community Cloud. The deployed app can be used immediately, as the API key is already configured on the server.