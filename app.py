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
st.markdown("*Developed by **Rudi Setiawan/FDovr19** | v1.9 Dynamic Essay Update*")
st.write("---")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    mapel_terpilih = st.multiselect("Pilih Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL)
    kkm = st.number_input("Batas Lulus (KKM)", value=75)
    
    st.divider()
    
    # STATISTIK
    total_user = dapatkan_statistik_pengunjung()
    st.subheader("🌐 Statistik Akses")
    st.metric(label="Pengguna Unik", value=f"{total_user} Perangkat")
    
    st.divider()
    
    # PROFIL DEVELOPER
    st.subheader("👨‍💻 Profil Pengembang")
    with st.container(border=True):
        st.markdown(f"""
        **Developer:** Rudi Setiawan  
        **Nickname:** FDovr19  
        **Lembaga:** SDN Duwet 2 Wates-Kediri  
        **Jabatan:** Operator  
        **Domisili:** Duwet, Wates-Kediri
        """)
    
    # KONTAK & SARAN
    st.subheader("📩 Kritik & Saran")
    st.link_button("📸 Instagram @rudi.juvent", "https://
