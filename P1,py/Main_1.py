import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. GENERATE 100K RANDOM DATA ---
n_rows = 100000
np.random.seed(42)

data = {
    'Timestamp': pd.date_range(start='2026-01-01', periods=n_rows, freq='min'),
    'Machine_ID': np.random.choice(['Turbine_A', 'Turbine_B', 'Turbine_C', 'Turbine_D'], n_rows),
    'Temperature': np.random.normal(loc=70, scale=15, size=n_rows), # Distribusi Normal
    'Energy_Output': np.random.uniform(200, 800, size=n_rows),     # Distribusi Uniform
    'Operating_Hours': np.random.randint(1, 24, size=n_rows)       # Bilangan Bulat
}

df = pd.DataFrame(data)
df.to_csv('energy_data_100k.csv', index=False)
print("✅ Berhasil membuat 'energy_data_100k.csv' dengan 100,000 baris!")

# --- 2. ANALISIS PANDAS + NUMPY  ---

# Hitung Efisiensi pake NumPy Vectorization (Cepat!)
# Rumus: (Energy / Operating Hours) - Penalti suhu jika > 85
df['Efficiency'] = df['Energy_Output'] / df['Operating_Hours']

# NumPy Power: np.where jauh lebih cepat dari .apply()
df['Status'] = np.where(df['Temperature'] > 85, 'OVERHEAT', 'NORMAL')

# Agregasi Statistik Cepat
print("\n--- RINGKASAN DATA ---")
print(df.groupby('Machine_ID')[['Temperature', 'Efficiency']].mean())

# Deteksi Anomali dengan NumPy
mean_temp = np.mean(df['Temperature'])
std_temp = np.std(df['Temperature'])
outlier_limit = mean_temp + (3 * std_temp) # 3-Sigma Rule

print(f"\nBatas Anomali Suhu: {outlier_limit:.2f}")
print(f"Jumlah Data Anomali: {np.sum(df['Temperature'] > outlier_limit)}")

# --- 3. VISUALISASI MATPLOTLIB ---

plt.figure(figsize=(12, 5))

# Plot Histogram Suhu buat liat distribusinya
plt.hist(df['Temperature'], bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(mean_temp, color='red', linestyle='dashed', linewidth=2, label='Mean')
plt.axvline(outlier_limit, color='orange', linestyle='dashed', linewidth=2, label='Anomali Limit')

plt.title('Distribusi Suhu Mesin (100k Data Points)', fontsize=14)
plt.xlabel('Temperature (C)')
plt.ylabel('Frekuensi')
plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
