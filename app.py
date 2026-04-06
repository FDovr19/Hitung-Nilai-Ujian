import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sistem Nilai Radar SD", layout="wide")

# 1. DATABASE MATA PELAJARAN
BANK_MAPEL = [
    "Agama", "Pancasila", "B. Indonesia", "Matematika", 
    "IPAS", "Seni Budaya", "PJOK", "B. Inggris", "Mulok", "Prakarya"
]

if 'database_nilai' not in st.session_state:
    st.session_state.database_nilai = []

st.title("🎓 Sistem Nilai & Analisis Radar")

# --- DATA SEKOLAH ---
with st.container(border=True):
    nama_sekolah = st.text_input("Nama Sekolah", placeholder="SD Negeri...", key="input_sekolah")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    mapel_terpilih = st.multiselect("Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL)
    kkm = st.number_input("KKM", value=75)
    st.divider()
    if st.button("🗑️ Reset Semua Data"):
        st.session_state.database_nilai = []
        st.rerun()

# --- FORM INPUT SISWA ---
st.write("---")
with st.container(border=True):
    st.subheader("📝 Input Data Siswa")
    c_nama, c_kelas = st.columns([3, 1])
    with c_nama:
        nama_input = st.text_input("Nama Lengkap", key="input_nama")
    with c_kelas:
        kelas_input = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], key="input_kelas")

    nilai_temp = {}
    if mapel_terpilih:
        st.write("---")
        cols = st.columns(2) # Bagi 2 kolom agar tidak terlalu panjang ke bawah
        for i, m in enumerate(mapel_terpilih):
            with cols[i % 2].expander(f"📖 {m}", expanded=False):
                # Input sederhana langsung nilai akhir untuk simulasi cepat
                n_akhir = st.number_input(f"Nilai Akhir {m}", min_value=0, max_value=100, value=0, key=f"n_{m}")
                nilai_temp[m] = n_akhir

        if st.button("➕ Simpan & Lihat Analisis", type="primary"):
            if not nama_sekolah or not nama_input:
                st.error("Lengkapi Nama Sekolah & Nama Siswa!")
            else:
                data_siswa = {"Sekolah": nama_sekolah, "Nama": nama_input, "Kelas": kelas_input}
                data_siswa.update(nilai_temp)
                data_siswa["Rata-rata"] = round(sum(nilai_temp.values()) / len(nilai_temp), 2)
                st.session_state.database_nilai.append(data_siswa)
                st.success(f"Data {nama_input} Berhasil Disimpan!")

# --- VISUALISASI RADAR (Siswa Terakhir) ---
if st.session_state.database_nilai:
    st.divider()
    last_siswa = st.session_state.database_nilai[-1]
    
    col_chart, col_stat = st.columns([2, 1])
    
    with col_chart:
        st.subheader(f"📊 Analisis Kekuatan: {last_siswa['Nama']}")
        # Menyiapkan data untuk Radar Chart
        categories = list(nilai_temp.keys())
        values = [last_siswa[m] for m in categories]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=last_siswa['Nama'],
            line_color='teal'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_stat:
        st.subheader("📈 Kesimpulan")
        st.metric("Rata-rata Siswa", f"{last_siswa['Rata-rata']}")
        lulus = [m for m, n in nilai_temp.items() if n >= kkm]
        gagal = [m for m, n in nilai_temp.items() if n < kkm]
        st.write(f"✅ **Lulus KKM:** {len(lulus)} Mapel")
        st.write(f"❌ **Remedial:** {len(gagal)} Mapel")

    # --- TABEL REKAP KESELURUHAN ---
    st.write("---")
    st.header("📋 Rekapitulasi Seluruh Siswa")
    df_rekap = pd.DataFrame(st.session_state.database_nilai)
    st.dataframe(df_rekap, use_container_width=True)
    
    csv = df_rekap.to_csv(index=False).encode('utf-8')
    st.download_button("📩 Download Data (.CSV)", data=csv, file_name="rekap_nilai.csv", mime="text/csv")
