import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Nilai Kolektif SD", layout="wide")

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

st.title("🎓 Kalkulator Nilai Kolektif (Multi-Siswa)")
st.write("Input nilai siswa satu per satu, lalu unduh rekapitulasi seluruh kelas di akhir.")

# --- SIDEBAR: PENGATURAN GLOBAL ---
with st.sidebar:
    st.header("⚙️ Pengaturan Ujian")
    mapel_terpilih = st.multiselect("Pilih Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL)
    kkm = st.number_input("Batas Lulus (KKM)", value=75)
    
    st.divider()
    if st.button("🗑️ Hapus Semua Data (Reset)"):
        st.session_state.database_nilai = []
        st.rerun()

# --- BAGIAN UTAMA: FORM INPUT SISWA ---
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
    for m in mapel_terpilih:
        with st.expander(f"📖 {m}", expanded=False):
            col_pg, col_es = st.columns(2)
            with col_pg:
                jml_pg = st.number_input(f"Total PG {m}", min_value=1, value=25, key=f"tpg_{m}")
                ben_pg = st.number_input(f"Benar PG {m}", min_value=0, max_value=jml_pg, key=f"bpg_{m}")
                bot_pg = st.number_input(f"Bobot PG {m}", value=1, key=f"opg_{m}")
            with col_es:
                jml_es = st.number_input(f"Total Essay {m}", min_value=0, value=5, key=f"tes_{m}")
                ben_es = st.number_input(f"Skor Essay {m}", min_value=0, key=f"bes_{m}")
                bot_es = st.number_input(f"Bobot Essay {m}", value=3, key=f"oes_{m}")
            
            # Hitung Nilai
            s_max = (jml_pg * bot_pg) + (jml_es * bot_es)
            s_perolehan = (ben_pg * bot_pg) + (ben_es * bot_es)
            skor_akhir = (s_perolehan / s_max) * 100 if s_max > 0 else 0
            nilai_temp[m] = round(skor_akhir, 2)

    # TOMBOL SIMPAN KE DATABASE
    if st.button("➕ Simpan & Tambah Siswa ke Daftar", type="primary"):
        if nama_input:
            data_siswa = {"Nama": nama_input, "Kelas": kelas_input}
            data_siswa.update(nilai_temp) # Gabungkan data diri dan nilai-nilainya
            data_siswa["Rata-rata"] = round(sum(nilai_temp.values()) / len(nilai_temp), 2)
            
            st.session_state.database_nilai.append(data_siswa)
            st.success(f"Data {nama_input} berhasil disimpan!")
        else:
            st.error("Nama siswa tidak boleh kosong!")

# --- BAGIAN BAWAH: REKAPITULASI KELAS ---
if st.session_state.database_nilai:
    st.divider()
    st.header("📊 Rekapitulasi Nilai Kelas")
    
    df_hasil = pd.DataFrame(st.session_state.database_nilai)
    
    # Tampilkan Tabel
    st.dataframe(df_hasil, use_container_width=True)
    
    # Ringkasan Kelas
    rata_kelas = df_hasil["Rata-rata"].mean()
    st.metric("Rata-rata Nilai Kelas", f"{rata_kelas:.2f}")

    # Tombol Download Seluruh Data
    csv = df_hasil.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📩 Download Rekap Nilai Seluruh Kelas (CSV)",
        data=csv,
        file_name=f"Rekap_Nilai_Kelas_{kelas_input}.csv",
        mime="text/csv",
    )
