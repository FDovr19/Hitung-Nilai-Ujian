import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kalkulator Nilai SD", layout="centered")

# --- DATABASE MATA PELAJARAN SD (SEDERHANA) ---
BANK_MAPEL = [
    "Pendidikan Agama dan Budi Pekerti",
    "Pendidikan Pancasila (PPKn)",
    "Bahasa Indonesia",
    "Matematika",
    "IPAS (IPA & IPS)",
    "Seni Budaya", # Gabungan semua cabang seni
    "PJOK (Olahraga)",
    "Bahasa Inggris",
    "Muatan Lokal (Bahasa Daerah)",
    "Prakarya"
]

st.title("🎓 Kalkulator Nilai Siswa SD")
st.write("Aplikasi penghitung nilai ujian berbobot untuk tingkat Sekolah Dasar.")

# --- SIDEBAR PENGATURAN ---
with st.sidebar:
    st.header("📋 Data Siswa")
    nama_siswa = st.text_input("Nama Siswa", placeholder="Contoh: Andi Pratama")
    kelas = st.selectbox("Kelas", ["1", "2", "3", "4", "5", "6"])
    
    st.divider()
    st.header("📚 Pilih Mata Pelajaran")
    mapel_terpilih = st.multiselect(
        "Pilih yang akan dinilai:",
        options=BANK_MAPEL,
        default=BANK_MAPEL
    )
    
    kkm = st.number_input("Batas Kelulusan (KKM)", value=75)

# --- LOGIKA INPUT NILAI ---
if not mapel_terpilih:
    st.info("💡 Pilih mata pelajaran di menu samping untuk menampilkan form nilai.")
else:
    hasil_akhir = []
    
    st.subheader(f"Input Nilai: {nama_siswa if nama_siswa else 'Siswa'} (Kelas {kelas})")
    
    for m in mapel_terpilih:
        with st.expander(f"📖 {m}", expanded=True):
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("**Pilihan Ganda (PG)**")
                jml_pg = st.number_input(f"Total Soal PG - {m}", min_value=1, value=25, key=f"tpg_{m}")
                ben_pg = st.number_input(f"Benar PG - {m}", min_value=0, max_value=jml_pg, key=f"bpg_{m}")
                bot_pg = st.number_input(f"Bobot per PG - {m}", value=1, key=f"opg_{m}")
                
            with c2:
                st.markdown("**Essay / Isian**")
                jml_es = st.number_input(f"Total Soal Essay - {m}", min_value=0, value=5, key=f"tes_{m}")
                ben_es = st.number_input(f"Skor Benar Essay - {m}", min_value=0, max_value=jml_es*10, key=f"bes_{m}")
                bot_es = st.number_input(f"Bobot per Essay - {m}", value=3, key=f"oes_{m}")

            # Rumus Perhitungan
            skor_max = (jml_pg * bot_pg) + (jml_es * bot_es)
            skor_perolehan = (ben_pg * bot_pg) + (ben_es * bot_es)
            
            nilai = (skor_perolehan / skor_max) * 100 if skor_max > 0 else 0
            
            hasil_akhir.append({
                "Mata Pelajaran": m,
                "Nilai": round(nilai, 2)
            })

    # --- TAMPILAN HASIL ---
    if hasil_akhir:
        st.divider()
        df = pd.DataFrame(hasil_akhir)
        rata_rata = df["Nilai"].mean()
        
        st.header("📊 Ringkasan Hasil")
        
        col1, col2 = st.columns(2)
        col1.metric("Rata-rata Keseluruhan", f"{rata_rata:.2f}")
        
        status = "TUNTAS ✅" if rata_rata >= kkm else "PERLU REMEDIAL ❌"
        col2.subheader(status)

        # Menampilkan Tabel
        st.table(df)

        # Tombol Simpan
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 Simpan ke Excel/CSV",
            data=csv,
            file_name=f"Nilai_{nama_siswa}_Kelas{kelas}.csv",
            mime="text/csv",
        )
