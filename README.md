
# 🧠 AI-Powered Skin Cancer Detection Portal

This is a web-based system that uses deep learning to classify skin lesions as cancerous or non-cancerous. If detected as cancerous, it further identifies the specific type of skin cancer.

## 🔍 Project Highlights

- **Binary Classification**: Lesion vs. Non-Lesion
- **Multi-Class Classification**: 7 cancer types using CNN
- **Web Interface**: Built with Streamlit
- **PDF Report**: Automatically generated and downloadable
- **Database Storage**: Stores patient data and image in PostgreSQL

## 🚀 Technologies Used

- Python, TensorFlow, Keras, Streamlit
- OpenCV, Pandas, NumPy, Matplotlib
- PostgreSQL (via psycopg2)
- FPDF for report generation

## 📁 Project Structure

```
skin-cancer-detection/
├── app3_fixed.py
├── Train_model_clean.ipynb
├── binary_model.keras
├── multiclass_model.keras
├── requirements.txt
├── README.md
├── sample_images/
│   ├── test_lesion.jpg
│   └── test_non_lesion.jpg
```

## 🧪 Try It Yourself

Upload a skin image and test the app:

- `sample_images/test_lesion.jpg` → Predicts lesion type
- `sample_images/test_non_lesion.jpg` → Predicts non-lesion

## 📥 How to Run

1. Clone the repo:
```bash
git clone https://github.com/your-username/skin-cancer-detection.git
cd skin-cancer-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app3_fixed.py
```

## 📸 Screenshots

> (You can include screenshots of app interface here)

## 👤 Author

**Bagurubilli Sai Kumar**  
[GitHub](https://github.com/MrSaikumar872) | [Email](mailto:bsaikumar872@gmail.com)

---

> This project was built as part of my MCA final project at Adikavi Nannaya University. It showcases AI’s potential in healthcare diagnostics.

## 🔗 Download Trained Models

Due to GitHub file size restrictions, the trained model files are hosted externally.

Please download and place them in your project directory before running the app:

| Model Type           | File Name                | Download Link |
|----------------------|--------------------------|----------------|
| Binary Classifier    | `binary_model.keras`     | [Download](https://drive.google.com/file/d/1DLnIjp00gPI0d3efXIQgj_bPbw63fpQB/view?usp=drive_link) |
| Multiclass Classifier| `multiclass_model.keras` | [Download](https://drive.google.com/file/d/1OxQAga4VMHo1cTMb9NMVTam9HyLxjJZH/view?usp=drive_link) |

📁 **Place both files in the same folder as your `app3_fixed.py` script.**

## 📸 Screenshots

### 🔹 Home Page
![Home Page](sample_images/)

### 🔹 Prediction Output
![Prediction](sample_images/)


