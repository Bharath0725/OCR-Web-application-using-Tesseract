import streamlit as st
from fpdf import FPDF
import base64
import requests
import cv2
import numpy as np
import pytesseract
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from docx import Document
from fpdf import FPDF
from streamlit_extras.stateful_button import button
import aspose.words as aw

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def download_image(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as out_file:
        out_file.write(r.content)

def process_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("removed_noise.png", img)
    cv2.imwrite(img_path, img)
    result = pytesseract.image_to_string(Image.open(img_path))
    return result

def save_to_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.ln(10)
    # pdf.cell(40, 10, text)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)

def save_to_docx(text, filename):
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    builder.writeln(text)
    doc.save(filename)

st.title("Image Downloader and OCR App")
st.write("This app downloads an image from a URL, processes it, and performs OCR on it.")
# Choose between URL and File Upload
option = st.selectbox("Choose Input Method:", ("URL", "Upload Image"))
if option == "URL":
    # Input URL
    url = st.text_input("Enter image URL:")
    extracted_text = ""

    if button("Download and Process Image", key="button1"):
        if url:
            filename = 'downloaded_image.jpg'
            download_image(url, filename)
            st.write("Image downloaded successfully!")
            st.image(filename, caption='Downloaded Image', use_column_width=True)
            st.write("Processing Image...")
            extracted_text = process_image(filename)
            st.write("Text Extracted from Image:")
            st.write(extracted_text)
            report_text = st.text_input("Report Text", value=extracted_text)
            if button("Save Edited Text", key="button2"):
                extracted_text = report_text
            extracted_textt = str(extracted_text)
            st.text(extracted_textt)

            save_format = st.selectbox("Choose save format", ["PDF", "DOCX"])

            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download file</a>'
            
            if extracted_textt:
                if button("Export Report", key="button3"):
                    if save_format == "PDF":
                        save_to_pdf(extracted_textt, "output.pdf")
                        st.markdown(create_download_link(open("output.pdf", "rb").read(), "output.pdf"), unsafe_allow_html=True)
                    elif save_format == "DOCX":
                        save_to_docx(extracted_textt, "output.docx")
                        st.markdown(create_download_link(open("output.docx", "rb").read(), "output.docx"), unsafe_allow_html=True)

else:
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    extracted_text = ""

    if button("Download and Process Image", key="buttonforsysupload1"):
        if uploaded_file is not None:
            img = Image.open(uploaded_file)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            img.save("uploaded_image.jpg")
            filename = 'uploaded_image.jpg'
            extracted_text = process_image(filename)
            st.write("Text Extracted from Image:")
            st.write(extracted_text)
            report_text = st.text_input("Report Text", value=extracted_text)
            if button("Save Edited Text", key="button2"):
                extracted_text = report_text
            extracted_textt = str(extracted_text)
            st.text(extracted_textt)

            save_format = st.selectbox("Choose save format", ["PDF", "DOCX"])

            def create_download_link(val, filename):
                b64 = base64.b64encode(val)  # val looks like b'...'
                return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}">Download file</a>'
            
            if extracted_textt:
                if button("Export Report", key="button3"):
                    if save_format == "PDF":
                        save_to_pdf(extracted_textt, "output.pdf")
                        st.markdown(create_download_link(open("output.pdf", "rb").read(), "output.pdf"), unsafe_allow_html=True)
                    elif save_format == "DOCX":
                        save_to_docx(extracted_textt, "output.docx")
                        st.markdown(create_download_link(open("output.docx", "rb").read(), "output.docx"), unsafe_allow_html=True)
