import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="KALKULATOR NILAI UJIAN", layout="wide")

# --- FUNGSI TRACKER PENGGUNA ---
def dapatkan_statistik_pengunjung():
    file_log = "pengunjung_unik.txt"
    try:
        ip_addr = st.context.headers.get("X-Forwarded-For", "127.0.0.1").split(',')[0]
    except:
        ip_addr = "127.0.0.1"
    if not os.path.exists(file_log):
        with open(file_log, "w") as f: f.write("")
    with open(file_log, "r") as f:
        daftar_ip = f.read().splitlines()
    if ip_addr not in daftar_ip and ip_addr != "127.0.0.1":
        with open(file_log, "a") as f:
            f.write(ip_addr + "\n")
        daftar_ip.append(ip_addr)
    return len(daftar_ip)

# 2. DATABASE
BANK_MAPEL = ["Agama", "Pancasila", "B. Indonesia", "Matematika", "IPAS", "Seni Budaya", "PJOK", "B. Inggris", "Mulok", "Prakarya"]

if 'database_nilai' not in st.session_state:
    st.session_state.database_nilai = []

# --- HEADER UTAMA ---
st.title("🧮 KALKULATOR NILAI UJIAN")
st.markdown("*Developed with ❤️ by **Rudi Setiawan/FDovr19** | v1.9.1 Fix Syntax*")
st.write("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    mapel_terpilih = st.multiselect("Pilih Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL)
    kkm = st.number_input("Batas Lulus (KKM)", value=75)
    
    st.divider()
    total_user = dapatkan_statistik_pengunjung()
    st.subheader("🌐 Statistik Akses")
    st.metric(label="Pengguna Unik", value=f"{total_user} Perangkat")
    
    st.divider()
    st.subheader("👨‍💻 Profil Pengembang")
    with st.container(border=True):
        st.markdown(f"""
        **Developer:** Rudi Setiawan  
        **Nickname:** FDovr19  
        **Lembaga:** SDN Duwet 2 Wates-Kediri  
        **Jabatan:** Operator  
        **Domisili:** Duwet, Wates-Kediri
        """)
    
    st.link_button("📸 Instagram @rudi.juvent", "https://www.instagram.com/rudi.juvent")
    
    st.divider()
    if st.button("🗑️ Reset Semua Data"):
        st.session_state.database_nilai = []
        st.rerun()

# --- INPUT DATA ---
with st.container(border=True):
    st.subheader("🏫 Data Sekolah & Siswa")
    nama_sekolah = st.text_input("Nama Sekolah", value="SDN Duwet 2 Wates Kediri")
    c_nama, c_kelas = st.columns([3, 1])
    with c_nama:
        nama_input = st.text_input("Nama Lengkap Siswa")
    with c_kelas:
        kelas_input = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"])

    if mapel_terpilih:
        st.write("---")
        
        nilai_temp = {}
        for m in mapel_terpilih:
            with st.expander(f"📖 {m}", expanded=False):
                # --- BAGIAN PG ---
                st.markdown("#### 🔵 Pilihan Ganda (PG)")
                c1, c2, c3 = st.columns(3)
                t_pg = c1.number_input(f"Total Soal PG ({m})", min_value=1, value=25, key=f"tpg_{m}")
                b_pg = c2.number_input(f"Benar PG ({m})", min_value=0, max_value=t_pg, key=f"bpg_{m}")
                p_pg = c3.number_input(f"Poin per PG ({m})", value=1, key=f"ppg_{m}")
                
                st.divider() 
                
                # --- BAGIAN ISIAN ---
                st.markdown("#### 🟢 Isian Singkat")
                c4, c5, c6 = st.columns(3)
                t_is = c4.number_input(f"Total Isian ({m})", min_value=0, value=10, key=f"tis_{m}")
                b_is = c5.number_input(f"Benar Isian ({m})", min_value=0, max_value=t_is, key=f"bis_{m}")
                p_is = c6.number_input(f"Poin per Isian ({m})", value=2, key=f"pis_{m}")
                
                st.divider() 
                
                # --- BAGIAN ESSAY (DYNAMIC TABLE) ---
                st.markdown("#### 🟠 Essay / Uraian")
                st.caption("Gunakan tabel di bawah untuk input nilai essay per nomor.")
                
                # Inisialisasi DataFrame awal
                df_awal = pd.DataFrame([{"Nomor": "1", "Skor": 0.0}])
                
                # Editor Tabel
                edited_df = st.data_editor(
                    df_awal,
                    num_rows="dynamic",
                    key=f"editor_{m}",
                    use_container_width=True,
                    column_config={
                        "Skor": st.column_config.NumberColumn("Nilai (0-100)", min_value=0, max_value=100, step=0.5)
                    }
                )
                
                # Kalkulasi Skor Essay
                total_skor_essay = edited_df["Skor"].sum()
                jumlah_soal_essay = len(edited_df)
                
                st.write("---")
                
                # LOGIKA NILAI AKHIR (CONTO
