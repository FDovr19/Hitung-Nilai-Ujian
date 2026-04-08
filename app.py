import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem Nilai SDN Duwet 2", layout="wide")

# --- FUNGSI TRACKER PENGGUNA UNIK ---
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

# 2. DATABASE & SESSION STATE
BANK_MAPEL = ["Agama", "Pancasila", "B. Indonesia", "Matematika", "IPAS", "Seni Budaya", "PJOK", "B. Inggris", "Mulok", "Prakarya"]

if 'database_nilai' not in st.session_state:
    st.session_state.database_nilai = []

# --- HEADER ---
st.title("🎓 Sistem Nilai Dashboard Pro")
st.markdown("*Developed with ❤️ by **Rudi Setiawan/FDovr** | v1.4 2026*")
st.write("---")

# --- SIDEBAR & KONTAK ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    mapel_terpilih = st.multiselect("Pilih Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL)
    kkm = st.number_input("Batas Lulus (KKM)", value=75)
    
    st.divider()
    
    # STATISTIK AKSES
    total_user = dapatkan_statistik_pengunjung()
    st.subheader("🌐 Statistik Akses")
    st.metric(label="Pengguna Unik", value=f"{total_user} Perangkat")
    
    st.divider()
    
    # KONTAK INSTAGRAM & KRITIK SARAN
    st.subheader("📩 Kritik & Saran")
    st.write("Punya masukan atau menemukan kendala?")
    # SILAKAN GANTI 'USER_IG_BAPAK' DENGAN USERNAME INSTAGRAM ASLI BAPAK
    username_ig = "USER_IG_BAPAK" 
    st.markdown(f"""
        <a href="https://instagram.com/rudi.juvent" target="_blank">
            <button style="border:none; border-radius:10px; padding:10px; background-color:#E1306C; color:white; cursor:pointer; width:100%;">
                📸 Hubungi via Instagram
            </button>
        </a>
    """, unsafe_allow_status=True)
    
    st.divider()
    if st.button("🗑️ Reset Semua Data"):
        st.session_state.database_nilai = []
        st.rerun()

# --- DATA SEKOLAH ---
with st.container(border=True):
    st.subheader("🏫 Informasi Satuan Pendidikan")
    nama_sekolah = st.text_input("Nama Sekolah", value="SDN Duwet 2 Wates Kediri")

# --- FORM INPUT SISWA ---
with st.container(border=True):
    st.subheader("📝 Input Data Siswa Baru")
    c_nama, c_kelas = st.columns([3, 1])
    with c_nama:
        nama_input = st.text_input("Nama Lengkap Siswa")
    with c_kelas:
        kelas_input = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"])

    if mapel_terpilih:
        st.write("---")
        # PETUNJUK PENGISIAN & TIPS
        with st.expander("💡 PETUNJUK PENGISIAN & TIPS (Wajib Baca)", expanded=False):
            st.markdown("""
            **Cara Mengisi Skor:**
            1.  **Total Soal:** Jumlah soal di naskah.
            2.  **Benar:** Jumlah soal yang dijawab benar oleh siswa.
            3.  **Poin per Butir:** Bobot nilai (Misal: PG=1, Isian=2, Essay=4).
            
            **Tips dari Sistem:**
            * Gunakan **Titik (.)** untuk angka desimal (Misal: 75.5).
            * Jika ada soal Essay dengan poin berbeda-beda, Bapak/Ibu bisa mengisi **Total Poin** yang didapat siswa di kolom 'Benar' dan isi angka '1' di kolom 'Poin'.
            * **Jangan lupa Download CSV** setelah selesai input agar data tersimpan permanen di laptop Bapak/Ibu.
            """)
        
        st.info("Masukkan skor tiap mata pelajaran di bawah ini:")
        
        nilai_temp = {}
        for m in mapel_terpilih:
            with st.expander(f"📖 {m}", expanded=False):
                col_pg, col_is, col_es = st.columns(3)
                with col_pg:
                    st.write("**PG**")
                    jml_pg = st.number_input(f"Total PG - {m}", min_value=1, value=25, key=f"tpg_{m}")
                    ben_pg = st.number_input(f"Benar PG - {m}", min_value=0, max_value=jml_pg, key=f"bpg_{m}")
                    bot_pg = st.number_input(f"Poin/PG - {m}", value=1, key=f"opg_{m}")
                with col_is:
                    st.write("**Isian**")
                    jml_is = st.number_input(f"Total Isian - {m}", min_value=0, value=10, key=f"tis_{m}")
                    ben_is = st.number_input(f"Benar Isian - {m}", min_value=0, max_value=jml_is, key=f"bis_{m}")
                    bot_is = st.number_input(f"Poin/Isian - {m}", value=2, key=f"ois_{m}")
                with col_es:
                    st.write("**Essay**")
                    jml_es = st.number_input(f"Total Essay - {m}", min_value=0, value=5, key=f"tes_{m}")
                    ben_es = st.number_input(f"Benar Essay - {m}", min_value=0, max_value=jml_es, key=f"bes_{m}")
                    bot_es = st.number_input(f"Poin/Essay - {m}", value=4, key=f"oes_{m}")
                
                s_max = (jml_pg * bot_pg) + (jml_is * bot_is) + (jml_es * bot_es)
                s_per = (ben_pg * bot_pg) + (ben_is * bot_is) + (ben_es * bot_es)
                nilai_akhir = (s_per / s_max) * 100 if s_max > 0 else 0
                nilai_temp[m] = round(nilai_akhir, 2)
                st.caption(f"Skor: {s_per}/{s_max} | Nilai: **{nilai_temp[m]}**")

        if st.button("➕ Simpan & Analisis Radar", type="primary"):
            if not nama_input:
                st.error("Nama siswa tidak boleh kosong!")
            else:
                data_siswa = {"Sekolah": nama_sekolah, "Nama": nama_input, "Kelas": kelas_input}
                data_siswa.update(nilai_temp)
                data_siswa["Rata-rata"] = round(sum(nilai_temp.values()) / len(nilai_temp), 2)
                st.session_state.database_nilai.append(data_siswa)
                st.success(f"Data {nama_input} Berhasil Disimpan!")

# --- VISUALISASI ---
if st.session_state.database_nilai:
    st.divider()
    df_rekap = pd.DataFrame(st.session_state.database_nilai)
    last_siswa = st.session_state.database_nilai[-1]
    
    col_chart, col_stat = st.columns([2, 1])
    with col_chart:
        st.subheader(f"📊 Radar Kompetensi: {last_siswa['Nama']}")
        categories = [m for m in mapel_terpilih if m in last_siswa]
        values = [last_siswa[m] for m in categories]
        if categories:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=values + [values[0]], theta=categories + [categories[0]], fill='toself', name=last_siswa['Nama'], line=dict(color='#1f77b4', width=3)))
            fig.add_trace(go.Scatterpolar(r=[kkm]*len(categories) + [kkm], theta=categories + [categories[0]], mode='lines', name='Batas KKM', line=dict(color='red', width=2, dash='dash')))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=True, height=450)
            st.plotly_chart(fig, use_container_width=True)

    with col_stat:
        st.subheader("📈 Auto-Insight")
        st.metric("Rata-rata", f"{last_siswa['Rata-rata']}")
        mapel_values = {m: last_siswa[m] for m in categories}
        if mapel_values:
            top_m = max(mapel_values, key=mapel_values.get)
            low_m = min(mapel_values, key=mapel_values.get)
            st.success(f"🌟 **Kekuatan:** {top_m}")
            if mapel_values[low_m] < kkm:
                st.error(f"⚠️ **Remedial:** {low_m}")
            else:
                st.warning(f"📘 **Saran:** Tingkatkan {low_m}")

    st.write("---")
    st.subheader("📋 Rekapitulasi Kolektif")
    st.dataframe(df_rekap, use_container_width=True)
    csv_data = df_rekap.to_csv(index=False, sep=';').encode('utf-8-sig')
    st.download_button(label="📩 Download Rekap untuk Excel (.CSV)", data=csv_data, file_name=f"Rekap_Nilai.csv", mime="text/csv")
