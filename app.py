import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sistem Nilai Sekolah Dasar", layout="wide")

# 1. DATABASE MATA PELAJARAN
BANK_MAPEL = [
    "Pendidikan Agama dan Budi Pekerti", "Pendidikan Pancasila (PPKn)",
    "Bahasa Indonesia", "Matematika", "IPAS (IPA & IPS)",
    "Seni Budaya", "PJOK (Olahraga)", "Bahasa Inggris",
    "Muatan Lokal (Bahasa Daerah)", "Prakarya"
]

# 2. INISIALISASI MEMORI (Session State)
if 'database_nilai' not in st.session_state:
    st.session_state.database_nilai = []

st.title("🎓 Sistem Input Nilai Kolektif")

# --- BAGIAN 1: DATA SEKOLAH (Paling Atas) ---
with st.container(border=True):
    st.subheader("🏫 Informasi Satuan Pendidikan")
    nama_sekolah = st.text_input("Nama Sekolah", placeholder="Contoh: SD Negeri 01 Merdeka", key="input_sekolah")

# --- BAGIAN 2: FORM INPUT SISWA ---
st.write("---")
with st.container(border=True):
    st.subheader("📝 Input Data Siswa Baru")
    c_nama, c_kelas = st.columns([3, 1])
    with c_nama:
        nama_input = st.text_input("Nama Lengkap Siswa", key="input_nama")
    with c_kelas:
        kelas_input = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], key="input_kelas")

    # Form dinamis untuk nilai
    nilai_temp = {}
    st.write("---")
    st.info("Ketuk mata pelajaran di bawah untuk mengisi skor:")
    for m in mapel_terpilih_input := st.sidebar.multiselect("Filter Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL):
        with st.expander(f"📖 {m}", expanded=False):
            col_pg, col_es = st.columns(2)
            with col_pg:
                st.caption("Pilihan Ganda")
                jml_pg = st.number_input(f"Total PG {m}", min_value=1, value=25, key=f"tpg_{m}")
                ben_pg = st.number_input(f"Benar PG {m}", min_value=0, max_value=jml_pg, key=f"bpg_{m}")
                bot_pg = st.number_input(f"Bobot PG {m}", value=1, key=f"opg_{m}")
            with col_es:
                st.caption("Essay/Isian")
                jml_es = st.number_input(f"Total Essay {m}", min_value=0, value=5, key=f"tes_{m}")
                ben_es = st.number_input(f"Skor Essay {m}", min_value=0, key=f"bes_{m}")
                bot_es = st.number_input(f"Bobot Essay {m}", value=3, key=f"oes_{m}")
            
            # Hitung Nilai per Mapel
            s_max = (jml_pg * bot_pg) + (jml_es * bot_es)
            s_perolehan = (ben_pg * bot_pg) + (ben_es * bot_es)
            skor_akhir = (s_perolehan / s_max) * 100 if s_max > 0 else 0
            nilai_temp[m] = round(skor_akhir, 2)

    # TOMBOL SIMPAN
    if st.button("➕ Simpan ke Tabel Rekap", type="primary"):
        if not nama_sekolah:
            st.error("Silakan isi Nama Sekolah terlebih dahulu!")
        elif not nama_input:
            st.error("Nama siswa tidak boleh kosong!")
        else:
            # Data yang disimpan ke database
            data_siswa = {
                "Sekolah": nama_sekolah,
                "Nama": nama_input, 
                "Kelas": kelas_input
            }
            data_siswa.update(nilai_temp)
            if nilai_temp:
                data_siswa["Rata-rata"] = round(sum(nilai_temp.values()) / len(nilai_temp), 2)
            
            st.session_state.database_nilai.append(data_siswa)
            st.success(f"Data {nama_input} berhasil disimpan!")

# --- SIDEBAR: PENGATURAN GLOBAL ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    kkm = st.number_input("Batas Lulus (KKM)", value=75)
    st.divider()
    if st.button("🗑️ Reset Semua Data"):
        st.session_state.database_nilai = []
        st.rerun()

# --- BAGIAN 3: REKAPITULASI KELAS ---
if st.session_state.database_nilai:
    st.divider()
    st.header("📊 Rekapitulasi Nilai")
    
    df_hasil = pd.DataFrame(st.session_state.database_nilai)
    
    # Menampilkan tabel kolektif
    st.dataframe(df_hasil, use_container_width=True)
    
    # Tombol Download
    csv = df_hasil.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📩 Download Hasil (.CSV)",
        data=csv,
        file_name=f"Rekap_Nilai_{nama_sekolah}.csv",
        mime="text/csv",
    )
