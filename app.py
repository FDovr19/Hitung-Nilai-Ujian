import streamlit as st
import pandas as pd

# Pengaturan halaman
st.set_page_config(page_title="Kalkulator Nilai SD", layout="centered")

# 1. DAFTAR MATA PELAJARAN SD
BANK_MAPEL = [
    "Pendidikan Agama dan Budi Pekerti",
    "Pendidikan Pancasila (PPKn)",
    "Bahasa Indonesia",
    "Matematika",
    "IPAS (IPA & IPS)",
    "Seni Budaya",
    "PJOK (Olahraga)",
    "Bahasa Inggris",
    "Muatan Lokal (Bahasa Daerah)",
    "Prakarya"
]

st.title("🎓 Kalkulator Nilai Siswa SD")

# --- BAGIAN ATAS: DATA SISWA ---
st.subheader("📋 Informasi Siswa")
col_nama, col_kelas = st.columns([3, 1]) # Nama lebih lebar dari Kelas

with col_nama:
    nama_siswa = st.text_input("Nama Lengkap Siswa", placeholder="Contoh: Andi Pratama")
with col_kelas:
    kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"])

st.divider()

# --- SIDEBAR: PENGATURAN MAPEL & KKM ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    mapel_terpilih = st.multiselect(
        "Pilih Mata Pelajaran:",
        options=BANK_MAPEL,
        default=BANK_MAPEL
    )
    
    kkm = st.number_input("Batas Lulus (KKM)", value=75)

# --- LOGIKA INPUT NILAI ---
if not mapel_terpilih:
    st.info("💡 Pilih mata pelajaran di menu samping (sidebar) untuk memulai.")
else:
    hasil_akhir = []
    
    st.write(f"### 📝 Input Nilai untuk {nama_siswa if nama_siswa else 'Siswa'}")
    
    for m in mapel_terpilih:
        # Expander agar tidak memakan tempat di layar HP
        with st.expander(f"📖 {m}", expanded=False):
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("**Pilihan Ganda (PG)**")
                jml_pg = st.number_input(f"Total Soal PG - {m}", min_value=1, value=25, key=f"tpg_{m}")
                ben_pg = st.number_input(f"Benar PG - {m}", min_value=0, max_value=jml_pg, key=f"bpg_{m}")
                bot_pg = st.number_input(f"Bobot per PG - {m}", value=1, key=f"opg_{m}")
                
            with c2:
                st.markdown("**Essay / Isian**")
                jml_es = st.number_input(f"Total Soal Essay - {m}", min_value=0, value=5, key=f"tes_{m}")
                # Untuk Essay, kita hitung skor mentah yang didapat
                ben_es = st.number_input(f"Skor Benar Essay - {m}", min_value=0, key=f"bes_{m}")
                bot_es = st.number_input(f"Bobot per Essay - {m}", value=3, key=f"oes_{m}")

            # Rumus Perhitungan
            skor_max = (jml_pg * bot_pg) + (jml_es * bot_es)
            skor_perolehan = (ben_pg * bot_pg) + (ben_es * bot_es)
            
            nilai = (skor_perolehan / skor_max) * 100 if skor_max > 0 else 0
            
            hasil_akhir.append({"Mata Pelajaran": m, "Nilai": round(nilai, 2)})

    # --- TAMPILAN HASIL AKHIR ---
    if hasil_akhir:
        st.divider()
        df = pd.DataFrame(hasil_akhir)
        rata_rata = df["Nilai"].mean()
        
        st.header("📊 Ringkasan Hasil")
        
        # Tampilan Ringkas
        c_res1, c_res2 = st.columns(2)
        c_res1.metric("Rata-rata", f"{rata_rata:.2f}")
        
        status = "TUNTAS ✅" if rata_rata >= kkm else "PERLU REMEDIAL ❌"
        c_res2.subheader(status)

        st.table(df)

        # Tombol Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Simpan Hasil ke CSV",
            data=csv,
            file_name=f"Nilai_{nama_siswa}_Kelas{kelas}.csv",
            mime="text/csv",
        )
