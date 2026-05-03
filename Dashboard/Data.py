import pandas as pd

def load_and_process_data(file_path):
    df = pd.read_csv(file_path)
    
    df['Tanggal'] = pd.to_datetime(df['Tanggal'])
    df['Bulan'] = df['Tanggal'].dt.to_period('M').astype(str)

    mothly_revenue = df.groupby('Bulan')['Total_Transaksi'].sum().reset_index()

    revenue_per_kategori = df.groupby('Kategori')['Total_Transaksi'].sum().reset_index()
    total_revenue = df['Total_Transaksi'].sum()

    total_piutang = df[df['Status'] == 'Hutang']['Total_Transaksi'].sum()
    total_kas = df[df['Status'] == 'Lunas']['Total_Transaksi'].sum()
    
    terlaris = df.groupby('Kategori')['Total_Transaksi'].count().sort_values(ascending=False).reset_index()
    kategori_paling_laris = terlaris.iloc[0]['Kategori'] if not terlaris.empty else "-"

    rata2_penjualan = df['Total_Transaksi'].mean().round()
    standar_deviasi = df['Total_Transaksi'].std().round() 

    

    return {
        'df_raw': df,
        'revenue_per_kategori': revenue_per_kategori,
        'total_revenue': total_revenue,
        'total_piutang': total_piutang,
        'total_kas' : total_kas,
        'terlaris': terlaris,
        'kategori_paling_laris': kategori_paling_laris,
        'rata2_penjualan': rata2_penjualan,
        'standar_deviasi': standar_deviasi,
        'monthly_rev' : mothly_revenue
    }