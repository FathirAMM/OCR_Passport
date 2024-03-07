import streamlit as st
from PIL import Image
from passporteye import read_mrz
import pytesseract
import re

# Configuration for Tesseract OCR
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
config = ('-l eng+sin+typew --oem 1 --psm 3')

# Function to extract MRZ data from the uploaded image
def extract_mrz_data(uploaded_image):
    mrz = read_mrz(uploaded_image)
    mrz_data = mrz.to_dict()

    # Clean NIC number
    if 'personal_number' in mrz_data:
        mrz_data['personal_number'] = re.sub('<{4}', '', mrz_data['personal_number'])

    return mrz_data

# Function to extract text from image using Pytesseract
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

# Main function to run the Streamlit app
def main():
  

    # Upload image
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Extract MRZ data
        mrz_data = extract_mrz_data(uploaded_image)

        # Extract text from image
        extracted_text = extract_text_from_image(image)

        # Check for the word "passport" in the extracted text
        if "passport" in extracted_text.lower():
            st.warning("🔍 Passport found! 🎉")
            

        # Display extracted MRZ data
        st.subheader("📝 MRZ Data 📋")
        st.write(f"**Names:** {mrz_data['names']}")
        st.write(f"**Surname:** {mrz_data['surname']}")
        st.write(f"**Nationality:** {mrz_data['nationality']}")
        st.write(f"**NIC Number:** {mrz_data['personal_number']}")
        st.write(f"**Passport Number:** {mrz_data['number']}")
        st.write(f"**Date of Birth:** {mrz_data['date_of_birth']}")
        st.write(f"**Expiration Date:** {mrz_data['expiration_date']}")
        st.write(f"**Sex:** {mrz_data['sex']}")
        st.write(f"**Type:** {mrz_data['type']}")
        st.write(f"**Raw Text:** {mrz_data['raw_text']}")

        # Extract text from image
        extracted_text = extract_text_from_image(image)

        # Check for the word "passport" in the extracted text
        if "passport" in extracted_text.lower():
            st.warning("🔍 Passport found! 🎉")

        # Expander to display extracted text
        with st.expander("🔍 Extracted Text"):
            st.write(extracted_text)

if __name__ == "__main__":
    main()
