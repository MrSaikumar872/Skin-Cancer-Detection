import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from fpdf import FPDF
from datetime import datetime
import os
from io import BytesIO
import psycopg2

# ✅ Load models
binary_model = tf.keras.models.load_model("C:/Users/Mr sai kumar/desktop/binary_model.keras")
multiclass_model = tf.keras.models.load_model("C:/Users/Mr sai kumar/desktop/best_multiclass_model.keras")

# ✅ Label mappings
multiclass_labels = {
    0: "akiec - Actinic keratoses",
    1: "bcc - Basal cell carcinoma",
    2: "bkl - Benign keratosis-like lesions",
    3: "df - Dermatofibroma",
    4: "mel - Melanoma",
    5: "nv - Melanocytic nevi",
    6: "vasc - Vascular lesions"
}

# ✅ Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="skincancerdb",
    user="postgres",            # Default pgAdmin user
    password="Bsk@8721"  # Replace this with your actual pgAdmin password
)
cursor = conn.cursor()


# ✅ Image Preprocessor
def preprocess_image(image, target_size):
    img = Image.open(image).convert("RGB")
    img = img.resize(target_size)
    img = np.array(img) / 255.0
    return np.expand_dims(img, axis=0)

# ✅ PDF Report Generator (fixed emoji issue)
def generate_pdf(binary_score, label, confidence, image_file, name, age, gender, notes):
    pdf = FPDF()
    pdf.add_page()

    img = Image.open(image_file).convert("RGB")
    img_path = "temp_image.jpg"
    img.save(img_path)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Skin Cancer Detection Report", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)

    pdf.image(img_path, x=10, y=30, w=80)
    pdf.ln(85)

    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(200, 10, txt=f"Date: {date_time}", ln=True)
    pdf.cell(200, 10, txt=f"Patient Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Age: {age}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {gender}", ln=True)
    pdf.cell(200, 10, txt=f"Lesion Probability: {binary_score:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Classification: {label}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {confidence:.2f}%", ln=True)

    if notes:
        pdf.multi_cell(0, 10, f"Additional Notes: {notes}")

    if confidence < 60.0:
        pdf.ln(10)
        pdf.set_text_color(255, 0, 0)
        pdf.multi_cell(0, 10, "Low Confidence Prediction.\nWe recommend consulting a dermatologist.")
        pdf.set_text_color(0, 0, 0)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_buffer = BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    if os.path.exists(img_path):
        os.remove(img_path)

    return pdf_buffer

def store_report(name, age, gender, binary_score, label, confidence, notes, pdf_data, image_name, image_file):
    insert_query = """
        INSERT INTO skin_reports 
        (name, age, gender, lesion_probability, classification, confidence, notes, report_pdf, image_name, image_file)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    # Read image bytes from the uploaded file
    image_bytes = image_file.read()
    
    cursor.execute(insert_query, (
        name,
        int(age),
        gender,
        float(binary_score),
        label,
        float(confidence),
        notes,
        pdf_data.read(),
        image_name,
        psycopg2.Binary(image_bytes)
    ))
    conn.commit()

# ✅ Fetch and view image from database
def fetch_image_by_name(name):
    fetch_query = """
        SELECT image_file FROM skin_reports 
        WHERE name = %s ORDER BY timestamp DESC LIMIT 1;
    """
    cursor.execute(fetch_query, (name,))
    result = cursor.fetchone()
    
    if result and result[0]:
        image_bytes = result[0]
        image = Image.open(BytesIO(image_bytes))
        return image
    return None


# ✅ Streamlit UI
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>🔬 AI Skin Cancer Detection</h1>", unsafe_allow_html=True)
st.markdown("Upload a skin image and fill patient details to get prediction and download a professional report.")

# ✅ Patient Info Inputs
with st.form("patient_form"):
    st.subheader("🧑 Patient Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        notes = st.text_area("Additional Notes")

    uploaded_file = st.file_uploader("📁 Upload Skin Image", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Analyze")

if submitted and uploaded_file:
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    with col2:
        st.write("⏳ Running Lesion Detection...")

        binary_input = preprocess_image(uploaded_file, (128, 128))
        binary_pred = binary_model.predict(binary_input, verbose=0)[0][0]

        st.write(f"🧪 Lesion Probability: `{binary_pred:.2f}`")

        if binary_pred <= 0.5:
            st.success("✅ Lesion Detected. Running Detailed Classification...")

            multiclass_input = preprocess_image(uploaded_file, (224, 224))
            multiclass_pred = multiclass_model.predict(multiclass_input, verbose=0)[0]
            class_index = np.argmax(multiclass_pred)
            class_label = multiclass_labels[class_index]
            confidence = multiclass_pred[class_index] * 100

            st.markdown(f"**🔍 Result:** `{class_label}`  \n**Confidence:** `{confidence:.2f}%`")

            if confidence < 60.0:
                st.warning("⚠️ Low confidence prediction. Please consult a dermatologist.")

            # Generate and download PDF Report
            pdf_data = generate_pdf(binary_pred, class_label, confidence, uploaded_file, name, age, gender, notes)
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_data,
                file_name=f"Skin_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )

            # ✅ Store report in PostgreSQL
            store_report(name, age, gender, binary_pred, class_label, confidence, notes, pdf_data, uploaded_file.name, uploaded_file)

        else:
            st.warning("❌ No lesion detected. The image appears to be Non-Lesion.")

# ✅ View uploaded image from DB
st.markdown("---")
st.subheader("🔎 View Stored Image from Database")

search_name = st.text_input("Enter patient name to view uploaded image:")

if st.button("Fetch Image"):
    result_img = fetch_image_by_name(search_name)
    
    if result_img:
        st.image(result_img, caption="Stored Image", use_container_width=True)
    else:
        st.warning("❌ No image found for this name.")
