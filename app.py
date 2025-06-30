import streamlit as st
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_index_page(titles, page_numbers):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, "Index Page")
    c.setFont("Helvetica", 12)
    y = 720
    for i, (title, page_num) in enumerate(zip(titles, page_numbers)):
        c.drawString(50, y, f"{i+1}. {title} ...... Page {page_num}")
        y -= 20
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

def merge_pdfs_with_index(uploaded_files):
    merger = PdfMerger()
    titles = [file.name for file in uploaded_files]
    page_numbers = []
    current_page = 1  # index is page 1

    for file in uploaded_files:
        reader = PdfReader(file)
        page_numbers.append(current_page + 1)  # PDFs start after index
        current_page += len(reader.pages)

    index_pdf = create_index_page(titles, page_numbers)
    merger.append(index_pdf)

    for i, file in enumerate(uploaded_files):
        merger.append(file, import_bookmarks=False)
        merger.add_outline_item(titles[i], page_numbers[i] - 1)

    output = BytesIO()
    merger.write(output)
    merger.close()
    output.seek(0)
    return output

st.title("📚 PDF Merger with Index and Navigation")
uploaded_files = st.file_uploader("Upload multiple PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("🔗 Merge PDFs with Index"):
        merged_pdf = merge_pdfs_with_index(uploaded_files)
        st.success("PDF merged successfully with index and outline!")
        st.download_button("📥 Download Merged PDF", merged_pdf, file_name="merged_with_index.pdf")
