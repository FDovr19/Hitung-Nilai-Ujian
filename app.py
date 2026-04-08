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
st.markdown("*Developed by **Rudi Setiawan/FDovr19** | v1.8 Profil Terupdate*")
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
        **Developer:** Rudi Setiawan, S. Kom.   
        **Nickname:** FDovr19  
        **Lembaga:** SDN Duwet 2 Wates-Kediri  
        **Jabatan:** Operator  
        **Domisili:** Duwet, Wates-Kediri
        """)
    
    # KONTAK & SARAN
    st.subheader("📩 Kritik & Saran")
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
        with st.expander("💡 PETUNJUK PENGISIAN & TIPS", expanded=False):
            st.markdown("""
            1. **Total Soal:** Jumlah soal di naskah.
            2. **Benar:** Jumlah soal yang dijawab benar.
            3. **Poin:** Bobot nilai (Misal: PG=1, Isian=2, Essay=4).
            4. Gunakan **Titik (.)** untuk desimal (Contoh: 80.5).
            """)
        
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
                
                # --- BAGIAN ESSAY ---
                st.markdown("#### 🟠 Essay / Uraian")
                c7, c8, c9 = st.columns(3)
                t_es = c7.number_input(f"Total Essay ({m})", min_value=0, value=5, key=f"tes_{m}")
                b_es = c8.number_input(f"Total Skor Benar ({m})", min_value=0, max_value=100, key=f"bes_{m}")
                p_es = c9.number_input(f"Poin ({m})", value=1, key=f"pes_{m}")
                
                st.write("---")
                
                # KALKULASI
                s_max = (t_pg * p_pg) + (t_is * p_is) + (t_es * p_es)
                s_per = (b_pg * p_pg) + (b_is * p_is) + (b_es * p_es)
                res = round((s_per / s_max) * 100, 2) if s_max > 0 else 0
                nilai_temp[m] = res
                st.markdown(f"**✅ Nilai Akhir {m}: {res}**")

        if st.button("➕ Simpan Data", type="primary"):
            if not nama_input:
                st.error("Nama siswa wajib diisi!")
            else:
                d_siswa = {"Sekolah": nama_sekolah, "Nama": nama_input, "Kelas": kelas_input}
                d_siswa.update(nilai_temp)
                d_siswa["Rata-rata"] = round(sum(nilai_temp.values()) / len(nilai_temp), 2)
                st.session_state.database_nilai.append(d_siswa)
                st.success(f"Data {nama_input} berhasil disimpan!")

# --- VISUALISASI ---
if st.session_state.database_nilai:
    st.divider()
    df = pd.DataFrame(st.session_state.database_nilai)
    last = st.session_state.database_nilai[-1]
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"📊 Radar: {last['Nama']}")
        cats = [m for m in mapel_terpilih if m in last]
        vals = [last[m] for m in cats]
        if cats:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=vals + [vals[0]], theta=cats + [cats[0]], fill='toself', name='Nilai'))
            fig.add_trace(go.Scatterpolar(r=[kkm]*len(cats) + [kkm], theta=cats + [cats[0]], mode='lines', name='KKM', line=dict(color='red', dash='dash')))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=400)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Insight")
        st.metric("Rata-rata Individu", f"{last['Rata-rata']}")
        m_vals = {m: last[m] for m in cats}
        if m_vals:
            t_m = max(m_vals, key=m_vals.get)
            l_m = min(m_vals, key=m_vals.get)
            st.success(f"🌟 Kekuatan: {t_m}")
            if m_vals[l_m] < kkm: st.error(f"⚠️ Remedial: {l_m}")

    st.write("---")
    st.subheader("📋 Tabel Rekap")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False, sep=';').encode('utf-8-sig')
    st.download_button("📩 Download Excel (.CSV)", data=csv, file_name="Rekap_Nilai.csv")
