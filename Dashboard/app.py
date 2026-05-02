import streamlit as st
from Data import load_and_process_data
from plots import plot_sunburst_donut, plot_revenue_bar

# 1. Konfigurasi Halaman (Wajib dipanggil pertama)
st.set_page_config(page_title="Sales Dashboard Dummy Data", page_icon="✨", layout="wide")

# 2. CSS Kustom untuk Background Fade Ungu & Styling Profesional
st.markdown("""
    <style>
    /* Background Gradient Ungu Gelap ke Muda */
    .stApp {
        background: linear-gradient(135deg, #130026 0%, #36005c 50%, #6818a5 100%);
        color: #ffffff;
    }
    /* Styling teks Header */
    h1, h2, h3 {
        color: #F8F8FF !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Styling Card untuk Metric / Statistik */
    div[data-testid="metric-container"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #BA55D3;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    /* Memaksa teks metrik menjadi putih/ungu muda */
    label[data-testid="stMetricLabel"] {
        color: #DDA0DD !important;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title(" Hardware Sales Executive Dashboard")
    st.markdown("Analisis performa penjualan dengan antarmuka visual kelas enterprise.")

    # Sidebar
    st.sidebar.markdown("### ⚙️ Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload dataset CSV", type=['csv'])

    if uploaded_file is not None:
        data = load_and_process_data(uploaded_file)

        # ---------------- GRID LAYOUT ----------------
        # Membagi layar menjadi 2 kolom (Kiri 60% : Kanan 40%)
        col_left, col_right = st.columns([6, 4])

        # === BAGIAN KIRI: VISUALISASI GRAFIK ===
        with col_left:
            # Atas: Sunburst (Donut)
            fig_sunburst = plot_sunburst_donut(data['terlaris'])
            st.plotly_chart(fig_sunburst, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True) # Jarak

            # Bawah: Bar Chart Gradasi
            fig_bar = plot_revenue_bar(data['revenue_per_kategori'])
            st.plotly_chart(fig_bar, use_container_width=True)

        # === BAGIAN KANAN: STATISTIK & TABEL ===
        with col_right:
            st.subheader("⚡ Statistik Utama")
            
            # Grid dalam grid untuk KPI
            kpi1, kpi2 = st.columns(2)
            kpi1.metric("Total Omset", f"Rp {data['total_revenue']:,.0f}")
            kpi2.metric("Rata-rata Penjualan", f"Rp {data['rata2_penjualan']:,.0f}")
            
            kpi3, kpi4 = st.columns(2)
            kpi3.metric("Produk Terlaris", data['kategori_paling_laris'])
            kpi4.metric("Deviasi Standar", f"Rp {data['standar_deviasi']:,.0f}")

            kpi5, kpi6 = st.columns(2)
            kpi5.metric("Total Kas", f"Rp {data['total_kas']:,.0f}")
            kpi6.metric("Total Piutang", f"Rp {data['total_piutang']:,.0f}")
            

            st.markdown("---")

            # Menampilkan info baris datastreamlit 
            st.caption(f"Total baris data diproses: {len(data['df_raw'])} baris.")

    else:
        st.info("Silakan masukkan file CSV pada panel di sebelah kiri untuk merender antarmuka.")

if __name__ == '__main__':
    main()