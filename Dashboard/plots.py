import plotly.express as px
import plotly.graph_objects as go

def plot_sunburst_donut(df_terlaris):
    """Membuat Sunburst / Donut chart (Bolong di tengah)"""
    fig = px.pie(
        df_terlaris, 
        values='Total_Transaksi', 
        names='Kategori', 
        hole=0.6, # Inilah yang membuatnya "bolong"
        color_discrete_sequence=['#FFFFFF', '#E6E6FA', '#D8BFD8', '#BA55D3', '#8A2BE2']
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#2b0054', width=2))
    )
    
    fig.update_layout(
        title=dict(text='Proporsi Penjualan Kategori', font=dict(size=20, color='white')),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, b=20, l=20, r=20),
        showlegend=False
    )
    return fig

def plot_revenue_bar(df_revenue):
    """Membuat Bar Chart dengan gradasi warna Ungu ke Putih"""
    # Diurutkan agar gradasi warnanya mengalir dengan indah
    df_revenue = df_revenue.sort_values('Total_Transaksi', ascending=True)
    
    fig = px.bar(
        df_revenue, 
        x='Kategori', 
        y='Total_Transaksi', 
        color='Total_Transaksi',
        # Color Scale: Ungu Gelap -> Ungu Muda -> Putih
        color_continuous_scale=['#4B0082', '#BA55D3', '#FFFFFF'], 
        text_auto='.2s'
    )
    
    fig.update_traces(
        textfont_size=14, 
        textangle=0, 
        textposition="outside", 
        cliponaxis=False,
        marker=dict(line=dict(color='rgba(0,0,0,0)', width=0))
    )
    
    fig.update_layout(
        title=dict(text='Omset Per Kategori', font=dict(size=20, color='white')),
        xaxis=dict(title='', tickfont=dict(color='white')),
        yaxis=dict(title='Total Transaksi (Rp)', tickfont=dict(color='white'), gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False, # Sembunyikan legenda gradasi agar UI lebih bersih
        margin=dict(t=50, b=20, l=20, r=20)
    )
    return fig