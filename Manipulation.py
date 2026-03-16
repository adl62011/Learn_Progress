#Anggap ada klien lu yang butuh bantuan. Tugas lu sekarang adalah membuat script tugas_analisis.py untuk memproses file tersebut.

#Misi Klien (Tugas lu):
#Cleaning (Pembersihan):
#- Hapus semua baris di mana kolom Jumlah bernilai <= 0 (ini data refund/error).
#- Isi semua nilai None (kosong) di kolom Produk dengan "Tanpa Nama" dan Kategori dengan "Umum".

#Manipulation:
#- Hitung kolom Total_Pendapatan (Jumlah * Harga).
#- Ubah kolom Tanggal menjadi format datetime.
  
#Filtering & Aggregation:
#- Filter hanya data dengan kategori "Elektronik" yang terjual lebih dari 5 unit.
#- Rekap Total Pendapatan per Produk.

#Reporting:
#- Simpan hasilnya ke file Hasil_Laporan_Analisis.xlsx.

import pandas as pd

file = 'contoh_pengolahan_file.xlsx'

# Cleaning data
df_final = (
    pd.read_excel(file)
    .query('Jumlah < 0')
    .assign(
        Produk = lambda x: x['Produk'].fillna('Tanpa nama'),
        Kategori = lambda x: x['Kategori'].fillna('Umum'),
        Total_Pendapatan = lambda x: x['Jumlah'] * x['Harga']
    )
    .query("Kategori == 'Elektronik' and Jumlah > 5")
    .groupby('Produk')['Total_Pendapatan'].sum()
    .reset_index()
)

df_final.to_excel('Hasil_Laporan_Analisis.xlsx', index=False)
print('"Analisis selesai! Cek file Hasil_Laporan_Analisis.xlsx"')



