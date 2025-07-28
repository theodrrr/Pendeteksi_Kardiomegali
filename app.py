import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import io, base64
import datetime
import time
import os
import gdown

st.set_page_config(
    page_title="Prediksi Kardiomegali X-ray Dada",
    page_icon="🫀",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        color-scheme: light !important;
        background: #f7f9fa !important;
        color: #222831 !important;
    }
    .stApp {
        background: #f7f9fa !important;
        color: #222831 !important;
    }
    /* Sidebar background and text */
    section[data-testid="stSidebar"] {
        background-color: #eaf6fb !important;
        color: #222831 !important;
    }
    /* Sidebar radio label (all states) */
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stRadio label span {
        color: #222831 !important;
        opacity: 1 !important;
        font-weight: 600 !important;
    }
    /* Sidebar radio selected */
    section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] > div:first-child {
        background: #4F8BF9 !important;
        border: 2px solid #4F8BF9 !important;
    }
    /* Sidebar radio unselected */
    section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] > div:first-child[aria-checked="false"] {
        background: #fff !important;
        border: 2px solid #4F8BF9 !important;
    }
    /* Sidebar title and custom text */
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] h4, 
    section[data-testid="stSidebar"] h5, 
    section[data-testid="stSidebar"] h6, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] li, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div {
        color: #222831 !important;
    }
    /* Remove unwanted opacity on sidebar */
    section[data-testid="stSidebar"] * {
        opacity: 1 !important;
    }
    .stMarkdown, .stMarkdown * {
        color: #222831 !important;
    }
    .st-bb, .st-bb * {
        color: #222831 !important;
    }
    .st-cq, .st-cq * {
        color: #222831 !important;
    }
    .stAlert, .stAlert * {
        color: #222831 !important;
    }
    .stButton>button {
        background-color: #4F8BF9 !important;
        color: white !important;
    }
    .stFileUploader>div>div {
        background: #e3eafc !important;
        border-radius: 8px !important;
    }
    .stSidebar {
        background-color: #e3eafc !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS untuk mempercantik tampilan
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    font-family: 'Poppins', 'Segoe UI', Arial, sans-serif !important;
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', 'Segoe UI', Arial, sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
}
.stApp {
    background: #f7f9fa !important;
}
.home-title {
    font-size: 2.8rem;
    color: #4F8BF9;
    font-weight: 700;
    margin-bottom: 0.5em;
    letter-spacing: 1px;
}
.card-blue {
    background: #eaf6fb;
    border-radius: 18px;
    box-shadow: 0 4px 24px #e3eafc;
    padding: 2.2em 2.5em 1.5em 2.5em;
    margin-bottom: 2em;
}
.card-yellow {
    background: #fffbe6;
    border-radius: 18px;
    box-shadow: 0 4px 24px #f7e9b0;
    padding: 2.2em 2.5em 1.5em 2.5em;
    margin-bottom: 2em;
}
.card-green {
    background: #eafaf1;
    border-radius: 18px;
    box-shadow: 0 4px 24px #b3e6c9;
    padding: 2.2em 2.5em 1.5em 2.5em;
    margin-bottom: 2em;
}
.card-pink {
    background: #fdeaea;
    border-radius: 18px;
    box-shadow: 0 4px 24px #f7c6c6;
    padding: 2.2em 2.5em 1.5em 2.5em;
    margin-bottom: 2em;
}
.card-purple {
    background: #f5eef8;
    border-radius: 18px;
    box-shadow: 0 4px 24px #e0c3f7;
    padding: 2.2em 2.5em 1.5em 2.5em;
    margin-bottom: 2em;
}
</style>
""", unsafe_allow_html=True)

# Percantik sidebar navigasi
sidebar_style = '''
    <style>
    .st-emotion-cache-1d3w5wq {background-color: #eaf6fb !important;}
    .sidebar-title {font-size:1.5em;font-weight:bold;color:#4F8BF9;margin-bottom:0.5em;display:flex;align-items:center;}
    .sidebar-menu {margin-bottom:1.5em;}
    .sidebar-menu label {display:flex;align-items:center;font-size:1.1em;padding:0.4em 0.7em;border-radius:8px;margin-bottom:0.2em;cursor:pointer;}
    .sidebar-menu label.selected {background:#4F8BF9;color:white;}
    .sidebar-menu label .icon {margin-right:0.7em;font-size:1.2em;}
    </style>
'''
st.markdown(sidebar_style, unsafe_allow_html=True)

# Sidebar navigasi hanya ikon besar, klik ikon untuk pindah halaman
sidebar_icon_style = '''
    <style>
    .sidebar-icon-nav {display:flex;justify-content:space-around;margin:1.5em 0 2em 0;}
    .sidebar-icon-btn {background:#eaf6fb;border:none;outline:none;border-radius:16px;padding:0.7em 0.9em;margin:0 0.2em;cursor:pointer;transition:box-shadow 0.2s;box-shadow:0 2px 8px #e3eafc;}
    .sidebar-icon-btn.selected {background:#4F8BF9;color:white;box-shadow:0 4px 16px #b3d6f7;}
    .sidebar-icon-btn:hover {background:#d6eaf8;}
    .sidebar-icon-btn span {font-size:2.1em;display:block;}
    </style>
'''
st.markdown(sidebar_icon_style, unsafe_allow_html=True)

# Tambahkan alert update penting dari pengembang di semua halaman
UPDATE_MESSAGE = '🚨 <b>Info Penting:</b> Aplikasi ini masih dalam tahap pengembangan. Selalu konsultasikan hasil ke dokter!'
st.markdown(f'<div style="background:#fffbe6;border-left:6px solid #f7ca18;padding:0.7em 1.2em;border-radius:8px;margin-bottom:1.2em;font-size:1.1em;">{UPDATE_MESSAGE}</div>', unsafe_allow_html=True)

# Load model dengan error handling
@st.cache_resource
def load_model():
    model_path = 'model.h5'
    gdrive_url = 'https://drive.google.com/uc?id=1TKZBYltovGYCaBIxk6Tg1mYbHQSq84v6'
    try:
        if not os.path.exists(model_path):
            with st.spinner('Mengunduh model dari Google Drive...'):
                gdown.download(gdrive_url, model_path, quiet=False)
        return tf.keras.models.load_model(model_path)
    except Exception as e:
        st.error(f"Model gagal dimuat: {e}")
        st.stop()

model = load_model()

def preprocess_image(image: Image.Image):
    # Convert to RGB if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)  # (1, 224, 224, 3)
    return img_array

# Tambahkan fungsi bantu untuk konversi gambar ke base64
def image_to_base64(img):
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()
    return base64.b64encode(byte_im).decode()

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=80)
    st.markdown('<div class="sidebar-title">🫀 Navigasi</div>', unsafe_allow_html=True)
    menu_items = [
        '🏠 Home',
        '🔎 Prediksi Kardiomegali',
        '❓ FAQ'
    ]
    page = st.radio('Pilih halaman:', menu_items, index=0)
    # Normalisasi value agar sesuai dengan logic halaman
    if page == '🏠 Home':
        page = 'Home'
    elif page == '🔎 Prediksi Kardiomegali':
        page = 'Prediksi Kardiomegali'
    elif page == '❓ FAQ':
        page = 'FAQ'
    st.markdown("---")
    st.markdown("""<small>Created by <b>Theodore Gabbelambok S</b> | Skripsi 2025</small>""", unsafe_allow_html=True)

if page == 'Home':
    st.markdown('<div class="home-title">🫀 Kardiomegali (Pembesaran Jantung)</div>', unsafe_allow_html=True)
    st.markdown('''
    <div class="card-blue">
        <h2>Apa Itu Kardiomegali?</h2>
        <p><b>Kardiomegali</b> adalah kondisi di mana jantung membesar melebihi ukuran normal. Ini biasanya terdeteksi melalui pemeriksaan X-ray dada. Kardiomegali bukanlah penyakit, melainkan tanda dari kondisi lain seperti hipertensi, penyakit katup jantung, atau kardiomiopati.</p>
        <div class="home-highlight">⚠️ <b>Info Penting:</b> Aplikasi ini masih dalam tahap pengembangan. Selalu konsultasikan hasil ke dokter!</div>
        <blockquote style="background:#fffbe6;padding:0.7em 1.5em;border-left:5px solid #4F8BF9;font-style:italic;">"Jantung yang sehat adalah kunci hidup yang berkualitas."</blockquote>
    </div>
    <div class="card-yellow">
        <h2>Seberapa Bahaya Kardiomegali?</h2>
        <ul>
            <li>Gagal jantung kronis</li>
            <li>Gangguan irama jantung (aritmia)</li>
            <li>Pembekuan darah yang bisa menyebabkan stroke</li>
            <li>Kematian mendadak</li>
        </ul>
    </div>
    <div class="card-green">
        <h2>Gejala yang Perlu Diwaspadai</h2>
        <ul>
            <li>Sesak napas, terutama saat aktivitas atau berbaring</li>
            <li>Nyeri dada</li>
            <li>Palpitasi (jantung berdebar)</li>
            <li>Kelelahan berlebihan</li>
            <li>Bengkak pada kaki atau pergelangan kaki</li>
        </ul>
    </div>
    <div class="card-pink">
        <h2>Penyebab Umum</h2>
        <ul>
            <li>Tekanan darah tinggi (hipertensi)</li>
            <li>Penyakit jantung koroner</li>
            <li>Kelainan katup jantung</li>
            <li>Kardiomiopati (penyakit otot jantung)</li>
            <li>Anemia berat</li>
            <li>Gangguan tiroid</li>
            <li>Infeksi pada jantung</li>
        </ul>
    </div>
    <div class="card-blue">
        <h2>Bagaimana Cara Mendeteksi?</h2>
        <ul>
            <li>Rontgen dada (X-ray)</li>
            <li>Echocardiogram (USG jantung)</li>
            <li>EKG (Elektrokardiogram)</li>
            <li>MRI jantung</li>
            <li>CT scan</li>
            <li>Pemeriksaan darah</li>
        </ul>
        <div class="home-funfact">💡 <b>Fun Fact:</b> Tidak semua pembesaran jantung bersifat permanen! Pada beberapa kasus, kardiomegali bisa membaik jika penyebab utamanya diatasi.</div>
    </div>
    <div class="card-yellow">
        <h2>Tips Pencegahan Kardiomegali</h2>
        <ul>
            <li>Kontrol tekanan darah secara rutin</li>
            <li>Jaga pola makan sehat (rendah garam, rendah lemak jenuh)</li>
            <li>Olahraga teratur sesuai anjuran dokter</li>
            <li>Hindari merokok dan konsumsi alkohol berlebihan</li>
            <li>Kelola stres dengan baik</li>
            <li>Rutin cek kesehatan jantung, terutama jika ada riwayat keluarga</li>
        </ul>
        <div class="home-tips">🏃‍♂️ <b>Tips Sehat:</b> Luangkan waktu 30 menit setiap hari untuk aktivitas fisik ringan seperti jalan kaki atau bersepeda.</div>
    </div>
    <div class="card-green">
        <h2>Langkah Jika Terdiagnosis Kardiomegali</h2>
        <ol>
            <li>Konsultasi ke dokter spesialis jantung untuk evaluasi lebih lanjut</li>
            <li>Ikuti anjuran pengobatan dan kontrol rutin</li>
            <li>Perbaiki gaya hidup (makan sehat, olahraga, cukup istirahat)</li>
            <li>Minum obat sesuai resep dokter</li>
            <li>Segera ke IGD jika mengalami sesak berat, nyeri dada hebat, atau pingsan</li>
        </ol>
    </div>
    <div class="card-purple">
        <h2>Sumber Referensi</h2>
        <ul>
            <li><a href="https://www.mayoclinic.org/diseases-conditions/enlarged-heart/symptoms-causes/syc-20355436" target="_blank">Mayo Clinic: Enlarged Heart (Cardiomegaly)</a></li>
            <li><a href="https://www.heart.org/en/health-topics/heart-failure/what-is-heart-failure/types-of-cardiomyopathy/enlarged-heart-cardiomegaly" target="_blank">American Heart Association: Enlarged Heart (Cardiomegaly)</a></li>
            <li><a href="https://www.alodokter.com/kardiomegali" target="_blank">Alodokter: Kardiomegali</a></li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)

elif page == 'Prediksi Kardiomegali':
    st.title('🔎 Prediksi Kardiomegali dari X-ray Dada')
    st.markdown('<div style="color:#4F8BF9;font-size:18px;font-weight:bold;">Langkah-langkah Prediksi:</div>', unsafe_allow_html=True)
    st.markdown('''
    <ol>
    <li>Upload Citra X-ray dada (format JPG/JPEG/PNG, grayscale).</li>
    <li>Klik tombol <b>Prediksi.</b></li>
    <li>Lihat hasil prediksi di bawah.</li>
    </ol>
    ''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader('UPLOAD CITRA X-RAY DADA DIBAWAH INI', type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Validasi gambar: minimal 100x100, channel 1/3, aspect ratio wajar
        if image.width < 100 or image.height < 100:
            st.error('Gambar terlalu kecil. Mohon upload gambar X-ray dengan resolusi lebih tinggi.')
        elif image.mode not in ['L', 'RGB']:
            st.error('Format gambar tidak didukung. Mohon upload gambar X-ray grayscale atau RGB.')
        elif image.width / image.height < 0.5 or image.width / image.height > 2:
            st.warning('Rasio gambar tidak umum untuk X-ray dada. Pastikan gambar yang diupload adalah X-ray dada.')
        else:
            # Validasi tambahan: deteksi dominasi grayscale (X-ray)
            img_arr = np.array(image.convert('RGB'))
            # Hitung selisih channel warna (semakin kecil, semakin grayscale)
            color_diff = np.abs(img_arr[:,:,0] - img_arr[:,:,1]) + np.abs(img_arr[:,:,1] - img_arr[:,:,2]) + np.abs(img_arr[:,:,0] - img_arr[:,:,2])
            mean_diff = np.mean(color_diff)
            if mean_diff > 15:
                st.error('Gambar yang diupload bukan citra X-ray dada (terlalu berwarna). Mohon upload citra X-ray dada yang valid.')
            else:
                st.markdown('<div style="display:flex;justify-content:center;">'
                            '<img src="data:image/png;base64,' + \
                            image_to_base64(image) + \
                            '" width="420" style="border-radius:10px;box-shadow:0 2px 8px #ccc;"/></div>',
                            unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)  # Tambahkan spasi vertikal sebelum tombol prediksi
                if st.button('Prediksi', use_container_width=True):
                    with st.spinner('Sedang memproses dan memprediksi...'):
                        progress_bar = st.progress(0)
                        for percent_complete in range(1, 101, 10):
                            time.sleep(0.05)
                            progress_bar.progress(percent_complete)
                        img_array = preprocess_image(image)
                        try:
                            prediction = model.predict(img_array)
                            progress_bar.progress(100)
                            progress_bar.empty()
                            pred_label = 'Kardiomegali' if prediction[0][0] > 0.5 else 'Normal'
                            color = '#e74c3c' if pred_label == 'Kardiomegali' else '#4F8BF9'
                            confidence = prediction[0][0] if pred_label == 'Kardiomegali' else 1 - prediction[0][0]
                            percent = confidence * 100
                            st.markdown(f'<div style="background:{color};color:white;padding:1em 2em;border-radius:10px;text-align:center;font-size:22px;font-weight:bold;">Hasil Prediksi: {pred_label}<br><span style="font-size:16px;">Keakuratan prediksi: {percent:.0f}%</span></div>', unsafe_allow_html=True)
                            st.caption('Keakuratan prediksi menunjukkan seberapa yakin model terhadap hasil yang ditampilkan.')
                            st.markdown('<hr>', unsafe_allow_html=True)
                            badge_icon = '✅' if pred_label == 'Normal' else '⚠️'
                            st.markdown(f'<div style="font-size:40px;text-align:center;">{badge_icon}</div>', unsafe_allow_html=True)
                            if pred_label == 'Kardiomegali':
                                st.markdown('<div style="background:#fdeaea;border-left:6px solid #e74c3c;padding:0.7em 1.2em;border-radius:8px;margin:1.2em 0 1.2em 0;font-size:1.1em;"><b>⚠️ Peringatan:</b> Hasil prediksi menunjukkan kemungkinan kardiomegali. Segera konsultasikan ke dokter spesialis jantung untuk pemeriksaan lebih lanjut.</div>', unsafe_allow_html=True)
                            if pred_label == 'Normal':
                                st.success('Citra X-ray terdeteksi **Normal**. Namun, hasil ini hanya sebagai alat bantu, bukan diagnosis medis pasti. Konsultasikan ke dokter untuk pemeriksaan lebih lanjut.')
                                st.markdown('''
<div style="background:#eaf6fb;padding:1.2em 2em;border-radius:14px;margin-bottom:1em;">
    <h4 style="color:#2980b9;margin-bottom:0.7em;">📝 Penjelasan:</h4>
    <ul style="font-size:17px;line-height:1.7;">
        <li>Hasil prediksi menunjukkan bahwa citra X-ray dada Anda <b>tidak terdeteksi adanya pembesaran jantung (kardiomegali)</b>.</li>
        <li>Meski hasil normal, tetap lakukan pemeriksaan kesehatan secara berkala, terutama jika Anda memiliki faktor risiko seperti hipertensi, diabetes, atau riwayat keluarga penyakit jantung.</li>
        <li>Jika Anda mengalami gejala seperti sesak napas, nyeri dada, atau kelelahan berlebihan, segera konsultasikan ke dokter.</li>
        <li>Hasil AI ini <b>tidak menggantikan pemeriksaan dan diagnosis dokter</b>.</li>
    </ul>
</div>
<div style="background:#d6eaf8;padding:1.2em 2em;border-radius:14px;">
    <h4 style="color:#2874a6;margin-bottom:0.7em;">💡 Tips Upload:</h4>
    <ul style="font-size:16px;line-height:1.7;">
        <li>Pastikan gambar X-ray jelas dan tidak buram.</li>
        <li>Format JPG/PNG, ukuran ideal 224x224 piksel.</li>
        <li>Jika gambar terlalu kecil/besar, sistem akan menyesuaikan otomatis.</li>
    </ul>
    <h4 style="color:#2874a6;margin-bottom:0.7em;">🔒 Catatan:</h4>
    <ul style="font-size:16px;line-height:1.7;">
        <li>Hasil prediksi ini berbasis AI dan tidak menggantikan diagnosis dokter.</li>
        <li>Data Anda <b>tidak disimpan</b> di server.</li>
    </ul>
</div>
''', unsafe_allow_html=True)
                            else:
                                st.warning('Citra X-ray terdeteksi **Kardiomegali**. Segera konsultasikan ke dokter spesialis jantung untuk pemeriksaan dan penanganan lebih lanjut.')
                                st.markdown('''
<div style="background:#fdeaea;padding:1.2em 2em;border-radius:14px;margin-bottom:1em;">
    <h4 style="color:#c0392b;margin-bottom:0.7em;">📝 Penjelasan:</h4>
    <ul style="font-size:17px;line-height:1.7;">
        <li>Hasil prediksi menunjukkan adanya <b>kemungkinan pembesaran jantung (kardiomegali)</b> pada citra X-ray dada Anda.</li>
        <li>Kardiomegali bisa menjadi tanda adanya masalah serius pada jantung, seperti gagal jantung, gangguan katup, atau tekanan darah tinggi yang tidak terkontrol.</li>
        <li>Segera lakukan konsultasi ke dokter spesialis jantung untuk pemeriksaan lanjutan (misal: echocardiogram, EKG, atau tes darah).</li>
        <li>Jangan panik, diagnosis pasti hanya dapat ditegakkan oleh dokter setelah pemeriksaan menyeluruh.</li>
        <li>Ikuti anjuran dokter dan lakukan perubahan gaya hidup sehat.</li>
    </ul>
</div>
<div style="background:#f9e79f;padding:1.2em 2em;border-radius:14px;">
    <h4 style="color:#b9770e;margin-bottom:0.7em;">💡 Tips Upload:</h4>
    <ul style="font-size:16px;line-height:1.7;">
        <li>Pastikan gambar X-ray jelas dan tidak buram.</li>
        <li>Format JPG/PNG, ukuran ideal 224x224 piksel.</li>
        <li>Jika gambar terlalu kecil/besar, sistem akan menyesuaikan otomatis.</li>
    </ul>
    <h4 style="color:#b9770e;margin-bottom:0.7em;">🔒 Catatan:</h4>
    <ul style="font-size:16px;line-height:1.7;">
        <li>Hasil prediksi ini berbasis AI dan tidak menggantikan diagnosis dokter.</li>
        <li>Data Anda <b>tidak disimpan</b> di server.</li>
    </ul>
</div>
''', unsafe_allow_html=True)
                            st.caption('Jika ingin mencoba gambar lain, silakan refresh halaman atau upload ulang.')
                            st.markdown('<hr>', unsafe_allow_html=True)
                            # Simpan riwayat prediksi di session state
                            if 'history' not in st.session_state:
                                st.session_state['history'] = []
                            st.session_state['history'].append({
                                'waktu': datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                                'label': pred_label,
                                'skor': f'{percent:.0f}%',
                                'file': uploaded_file.name
                            })
                        except Exception as e:
                            progress_bar.empty()
                            st.error(f"Prediksi gagal: {e}")
                # Tampilkan riwayat prediksi
                if 'history' in st.session_state and len(st.session_state['history']) > 0:
                    st.markdown('---')
                    st.subheader('Riwayat Prediksi Sesi Ini')
                    for item in reversed(st.session_state['history']):
                        st.markdown(f"<div style='background:#f7f9fa;padding:0.5em 1em;border-radius:8px;margin-bottom:6px;'><b>{item['label']}</b> ({item['skor']})<br><span style='font-size:12px;color:#888;'>{item['waktu']} | {item['file']}</span></div>", unsafe_allow_html=True)
    else:
        st.info('Silakan upload foto X-ray dada untuk melakukan prediksi.')

    # Footer bantuan di paling bawah halaman
    st.markdown('<hr>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;font-size:14px;">Butuh bantuan? Hubungi: <a href="mailto:admin@email.com">admin@email.com</a></div>', unsafe_allow_html=True)
    st.markdown('<hr>', unsafe_allow_html=True)

# Halaman FAQ
if page == 'FAQ':
    st.markdown('<div style="display:flex;align-items:center;margin-bottom:1em;"><span style="font-size:2.2em;margin-right:10px;">❓</span><span style="font-size:2em;font-weight:bold;color:#4F8BF9;">FAQ (Frequently Asked Questions)</span></div>', unsafe_allow_html=True)
    st.markdown('''<div style="margin-bottom:1.5em;font-size:18px;">Berikut beberapa pertanyaan yang sering diajukan seputar aplikasi dan kardiomegali.</div>''', unsafe_allow_html=True)
    faq_cards = [
        {'color':'#eaf6fb', 'border':'#4F8BF9', 'icon':'🫀', 'q':'Apa itu kardiomegali?', 'a':'''Kardiomegali adalah kondisi di mana ukuran jantung lebih besar dari normal. Ini bukan penyakit utama, melainkan tanda adanya masalah lain pada jantung, seperti tekanan darah tinggi, penyakit katup jantung, atau kardiomiopati. Kardiomegali biasanya terdeteksi melalui pemeriksaan X-ray dada, echocardiogram (USG jantung), atau MRI.\n\n<b>Kenapa bisa terjadi?</b>\n- Jantung membesar karena harus bekerja lebih keras dari biasanya, misalnya akibat tekanan darah tinggi yang tidak terkontrol.\n- Bisa juga karena kelainan katup, infeksi, atau kelainan otot jantung.\n\n<b>Apakah kardiomegali berbahaya?</b>\n- Jika tidak ditangani, kardiomegali dapat menyebabkan gagal jantung, gangguan irama jantung, atau komplikasi lain.\n- Namun, dengan penanganan yang tepat, banyak orang dengan kardiomegali dapat hidup sehat dan aktif.'''},
        {'color':'#eafaf1', 'border':'#27ae60', 'icon':'🤖', 'q':'Apakah hasil prediksi aplikasi ini bisa dijadikan diagnosis pasti?', 'a':'''Tidak. Hasil prediksi dari aplikasi ini <b>hanya sebagai alat bantu dan edukasi</b>.\n\n<b>Kenapa tidak bisa jadi diagnosis pasti?</b>\n- Model AI hanya menganalisis gambar X-ray berdasarkan data yang pernah dipelajari.\n- Diagnosis pasti membutuhkan pemeriksaan fisik, wawancara medis, dan tes penunjang lain oleh dokter.\n- Ada kemungkinan hasil prediksi salah (false positive/false negative).\n\n<b>Saran:</b>\n- Selalu konsultasikan hasil prediksi ke dokter, terutama jika Anda memiliki gejala atau riwayat penyakit jantung.'''},
        {'color':'#fffbe6', 'border':'#f7ca18', 'icon':'📤', 'q':'Bagaimana cara upload gambar X-ray yang benar?', 'a':'''<b>Tips upload gambar X-ray:</b>\n- Pastikan gambar X-ray jelas, tidak buram, dan tidak terpotong.\n- Gunakan format JPG, JPEG, atau PNG.\n- Ukuran ideal 224x224 piksel, namun sistem akan menyesuaikan otomatis jika ukuran berbeda.\n- Hindari mengupload foto hasil scan dokumen atau foto dari layar komputer, karena kualitasnya bisa menurun.\n\n<b>Contoh gambar yang baik:</b>\n- Gambar X-ray dada yang seluruh area paru-paru dan jantung terlihat jelas.'''},
        {'color':'#fdeaea', 'border':'#e74c3c', 'icon':'🔒', 'q':'Apakah data gambar saya disimpan di server?', 'a':'''Tidak. Semua proses prediksi dilakukan secara lokal di komputer Anda.\n\n<b>Penjelasan:</b>\n- Gambar yang Anda upload tidak dikirim ke server atau disimpan oleh pengembang aplikasi.\n- Setelah prediksi selesai, data gambar tidak tersimpan di mana pun.\n\n<b>Keamanan data Anda adalah prioritas kami.</b>'''},
        {'color':'#f9e79f', 'border':'#f39c12', 'icon':'⚠️', 'q':'Apa yang harus dilakukan jika hasil prediksi menunjukkan kardiomegali?', 'a':'''<b>Langkah yang harus dilakukan:</b>\n1. Jangan panik. Hasil AI bukan diagnosis pasti.\n2. Segera konsultasikan ke dokter spesialis jantung untuk pemeriksaan lebih lanjut (misal: echocardiogram, EKG, tes darah).\n3. Ikuti saran dan pengobatan dari dokter.\n4. Jaga pola hidup sehat: makan bergizi, olahraga teratur, hindari rokok dan alkohol.\n\n<b>Catatan:</b>\n- Diagnosis pasti hanya dapat ditegakkan oleh dokter setelah pemeriksaan menyeluruh.\n- Jika Anda mengalami sesak napas berat, nyeri dada hebat, atau pingsan, segera ke IGD.'''},
        {'color':'#fbeee6', 'border':'#e67e22', 'icon':'💸', 'q':'Apakah aplikasi ini gratis?', 'a':'''Ya, aplikasi ini <b>gratis</b> dan dibuat untuk tujuan edukasi serta membantu masyarakat mengenal risiko kardiomegali.\n\n<b>Anda bebas menggunakan aplikasi ini tanpa biaya apa pun.</b>\n\nJika aplikasi ini bermanfaat, silakan bagikan ke teman atau keluarga yang membutuhkan.'''},
    ]
    for card in faq_cards:
        st.markdown(f'''<div style="margin-bottom:1.2em;">
            <div style="display:inline-block;background:{card['color']};border-left:8px solid {card['border']};border-radius:10px 10px 10px 10px;padding:0.5em 1.2em 0.5em 1.2em;font-weight:bold;font-size:1.1em;">{card['icon']} {card['q']}</div>
        </div>''', unsafe_allow_html=True)
        with st.expander('Lihat jawaban'):
            st.markdown(card['a'], unsafe_allow_html=True) 
