import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Sistem Nilai SDN Duwet 2", layout="wide")

# 2. DATABASE & SESSION STATE
BANK_MAPEL = [
    "Agama", "Pancasila", "B. Indonesia", "Matematika", 
    "IPAS", "Seni Budaya", "PJOK", "B. Inggris", "Mulok", "Prakarya"
]

if 'database_nilai' not in st.session_state:
    st.session_state.database_nilai = []

# --- HEADER & KREDIT ---
st.title("🎓 Sistem Nilai Dashboard Pro")
st.markdown("*Developed with ❤️ by **Rudi Setiawan/FDovr** | v1.2 2026*")
st.write("---")

# --- DATA SEKOLAH ---
with st.container(border=True):
    st.subheader("🏫 Informasi Satuan Pendidikan")
    nama_sekolah = st.text_input("Nama Sekolah", value="SDN Duwet 2 Wates Kediri", key="input_sekolah")

# --- SIDEBAR & PENGATURAN ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    mapel_terpilih = st.multiselect("Pilih Mata Pelajaran:", options=BANK_MAPEL, default=BANK_MAPEL)
    kkm = st.number_input("Batas Lulus (KKM)", value=75)
    
    st.divider()
    if st.button("🗑️ Reset Semua Data"):
        st.session_state.database_nilai = []
        st.rerun()
    
    st.divider()
    if st.button("ℹ️ Tentang Pengembang"):
        st.dialog("Profil Pengembang")
        st.markdown(f"""
        ### 👨‍💻 Developer Profile
        **Nama:** Rudi Setiawan/FDovr  
        **Jabatan:** Katanya Operator  
        **Instansi:** SDN Duwet 2 Wates Kediri
        
        ---
        **Catatan:** Aplikasi ini dikembangkan secara mandiri untuk membantu digitalisasi rekapitulasi nilai di lingkungan **SDN Duwet 2 Wates Kediri**.
        """)

# --- FORM INPUT SISWA ---
with st.container(border=True):
    st.subheader("📝 Input Data Siswa Baru")
    c_nama, c_kelas = st.columns([3, 1])
    with c_nama:
        nama_input = st.text_input("Nama Lengkap Siswa", key="input_nama")
    with c_kelas:
        kelas_input = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"], key="input_kelas")

    nilai_temp = {}
    if mapel_terpilih:
        st.write("---")
        st.info("Input skor detail mata pelajaran di bawah:")
        for m in mapel_terpilih:
            with st.expander(f"📖 {m}", expanded=False):
                col_pg, col_is, col_es = st.columns(3)
                with col_pg:
                    st.markdown("**PG**")
                    jml_pg = st.number_input(f"Total PG - {m}", min_value=1, value=25, key=f"tpg_{m}")
                    ben_pg = st.number_input(f"Benar PG - {m}", min_value=0, max_value=jml_pg, key=f"bpg_{m}")
                    bot_pg = st.number_input(f"Poin/PG - {m}", value=1, key=f"opg_{m}")
                with col_is:
                    st.markdown("**Isian**")
                    jml_is = st.number_input(f"Total Isian - {m}", min_value=0, value=10, key=f"tis_{m}")
                    ben_is = st.number_input(f"Benar Isian - {m}", min_value=0, max_value=jml_is, key=f"bis_{m}")
                    bot_is = st.number_input(f"Poin/Isian - {m}", value=2, key=f"ois_{m}")
                with col_es:
                    st.markdown("**Essay**")
                    jml_es = st.number_input(f"Total Essay - {m}", min_value=0, value=5, key=f"tes_{m}")
                    ben_es = st.number_input(f"Jml Benar Essay - {m}", min_value=0, max_value=jml_es, key=f"bes_{m}")
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

            # --- VISUALISASI RADAR & ANALISIS OTOMATIS ---
if st.session_state.database_nilai:
    st.divider()
    df_rekap = pd.DataFrame(st.session_state.database_nilai)
    last_siswa = st.session_state.database_nilai[-1]
    
    col_chart, col_stat = st.columns([2, 1])
    
    with col_chart:
        st.subheader(f"📊 Radar Kompetensi: {last_siswa['Nama']}")
        # Filter hanya mapel yang ada nilainya di data siswa terakhir
        categories = [m for m in mapel_terpilih if m in last_siswa]
        values = [last_siswa[m] for m in categories]
        
        if categories:
            fig = go.Figure()

            # 1. Area Nilai Siswa
            fig.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=last_siswa['Nama'],
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8)
            ))

            # 2. Garis KKM
            fig.add_trace(go.Scatterpolar(
                r=[kkm]*len(categories) + [kkm],
                theta=categories + [categories[0]],
                mode='lines',
                name='Batas KKM',
                line=dict(color='red', width=2, dash='dash')
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="center", x=0.5),
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_stat:
        st.subheader("📈 Auto-Insight")
        st.metric("Rata-rata Individu", f"{last_siswa['Rata-rata']}")
        
        # Ambil nilai mapel saja untuk analisis
        mapel_values = {m: last_siswa[m] for m in categories}
        if mapel_values:
            top_mapel = max(mapel_values, key=mapel_values.get)
            low_mapel = min(mapel_values, key=mapel_values.get)
            
            st.success(f"🌟 **Kekuatan Utama:**\n{top_mapel} ({mapel_values[top_mapel]})")
            
            if mapel_values[low_mapel] < kkm:
                st.error(f"⚠️ **Perlu Remedial:**\n{low_mapel} ({mapel_values[low_mapel]})")
            else:
                st.warning(f"📘 **Saran:**\nTingkatkan {low_mapel} ({mapel_values[low_mapel]})")

    # --- TABEL REKAP (VERSI PALING AMAN) ---
    st.write("---")
    st.subheader("📋 Rekapitulasi Kolektif")
    
    # Tampilkan tabel biasa (Tanpa styling warna yang bikin error)
    st.dataframe(df_rekap, use_container_width=True)
    
    # Tombol Download
    csv = df_rekap.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📩 Download Rekap Nilai (.CSV)",
        data=csv,
        file_name=f"Rekap_Nilai_SDN_Duwet_2.csv",
        mime="text/csv"
    )
