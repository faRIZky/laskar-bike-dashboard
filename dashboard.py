import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Bike Sharing Dashboard")

# Set theme
sns.set_theme(style="whitegrid")

# Load data
bike_df = pd.read_csv("bike.csv")

# Sidebar
with st.sidebar:
    st.title("🚴 Bike Sharing Dashboard")
    st.markdown("""
    **Fitur Dashboard:**
    - Rata-rata peminjaman per musim
    - Perbandingan pengguna terdaftar dan tidak terdaftar
    - Distribusi peminjaman pada hari kerja & libur
    - Clustering peminjaman berdasarkan jam
    """)
    st.info("Gunakan fitur interaktif untuk eksplorasi lebih lanjut!")

# Header
st.header("Bike Sharing Dashboard 🚲")

# Warna untuk musim
season_colors = ['#76c7c0', '#ffcc5c', '#ff6f61', '#6b5b95']

# Bar chart: Mean Bike Rental Count by Season
st.subheader("Bagaimana rata-rata peminjaman pada setiap musim?")
avg_season_df = bike_df.groupby('season')['count'].mean()
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(avg_season_df.index, avg_season_df.values, color=season_colors)
ax.set_xticks([1, 2, 3, 4])
ax.set_xticklabels(['Spring', 'Summer', 'Fall', 'Winter'])
ax.set_title('Mean Bike Rental Count by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Average Rental Count')
st.pyplot(fig)

with st.expander("Lihat penjelasan"):
    st.write("""
    Data menunjukan bahwa rata-rata permintaan peminjaman sepeda tertinggi terjadi di musim gugur dan permintaan terendah terjadi di musim semi. Ketiga musim lainnya terlihat berada di antara angka 200, sedangkan musim semi tidak sampai rata-rata 150 permintaan.
    """)

# Subplot: Mean Registered vs. Unregistered Users
st.subheader("Bagaimana perbedaan peminjaman antara pengguna terdaftar dan tidak terdaftar?")
avg_registered_df = bike_df.groupby('year')['registered'].mean()
avg_unregistered_df = bike_df.groupby('year')['unregistered'].mean()
fig, ax = plt.subplots(1, 2, figsize=(16, 6))
ax[0].bar(avg_registered_df.index, avg_registered_df.values, color="#4C72B0")
ax[0].set_title('Mean Rental Count by Registered Users')
ax[0].set_xlabel('Year')
ax[0].set_ylabel('Average Registered Users')
ax[1].bar(avg_unregistered_df.index, avg_unregistered_df.values, color="#DD8452")
ax[1].set_title('Mean Rental Count by Unregistered Users')
ax[1].set_xlabel('Year')
ax[1].set_ylabel('Average Unregistered Users')
st.pyplot(fig)

with st.expander("Lihat penjelasan"):
    st.write("""
    Total rata-rata permintaan peminjaman pada tahun 2021 lebih tinggi. Hal ini juga sebanding lurus dengan naiknya jumlah permintaan dari pengguna unregistered sebesar 48.28%. Walaupun begitu, gap nilai registered dan unregistered sangatlah jauh. Angka unregistered tidak menyentuh angka 100 pada tahun 2020 dan 2021.
    """)

# Pie Chart: Weekday Distribution for Holiday
st.subheader("Bagaimana distribusi peminjaman sepeda pada hari kerja dan hari libur?")
weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
holiday_0 = bike_df[bike_df['holiday'] == 0]
holiday_1 = bike_df[bike_df['holiday'] == 1]
weekday_counts_0 = holiday_0['weekday'].value_counts().sort_index()
weekday_counts_1 = holiday_1['weekday'].value_counts().sort_index()
colors = sns.color_palette("Set2")
fig, ax = plt.subplots(1, 2, figsize=(14, 6))
ax[0].pie(weekday_counts_0, labels=[weekday_names[idx] for idx in weekday_counts_0.index], autopct='%1.1f%%', colors=colors)
ax[0].set_title('Weekday Distribution (Non-Holiday)')
ax[1].pie(weekday_counts_1, labels=[weekday_names[idx] for idx in weekday_counts_1.index], autopct='%1.1f%%', colors=colors)
ax[1].set_title('Weekday Distribution (Holiday)')
st.pyplot(fig)

with st.expander("Lihat penjelasan"):
    st.write("""
    Permintaan cenderung stabil pada hari kerja, tetapi meningkat pada hari libur, terutama pada hari Selasa. Hal ini mungkin karena adanya acara khusus atau promosi yang menarik lebih banyak pengguna.
    """)

# Clustering Visualization
st.subheader("Bagaimana pola peminjaman berdasarkan jam dengan clustering?")
features = ['hour', 'season', 'count']
bike_cluster_df = bike_df[features]
scaler = StandardScaler()
bike_cluster_scaled = scaler.fit_transform(bike_cluster_df)
kmeans = KMeans(n_clusters=3, init='k-means++', random_state=42)
bike_df['Cluster'] = kmeans.fit_predict(bike_cluster_scaled)
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=bike_df['hour'], y=bike_df['count'], hue=bike_df['Cluster'], palette='Dark2', s=50, ax=ax)
ax.set_xlabel('Hour')
ax.set_ylabel('Bike Rental Count')
ax.set_title('Clustering of Bike Rentals by Hour')
st.pyplot(fig)

with st.expander("Lihat penjelasan"):
    st.write("""

Berdasarkan metode WCSS, jumlah cluster optimal untuk segmentasi data adalah tiga cluster.
- Cluster 0 (biru kehijauan): Terjadi pada jam-jam dengan jumlah rental rendah, biasanya saat dini hari atau malam.
- Cluster 1 (kuning): Mewakili waktu transisi dengan volume rental sedikit lebih tinggi, seperti pagi sebelum jam sibuk atau sore menjelang malam.
- Cluster 2 (ungu): Menunjukkan jam-jam sibuk dengan lonjakan signifikan dalam penyewaan sepeda, terutama pada pagi (07:00–09:00) dan sore (17:00–19:00), yang kemungkinan besar terkait dengan jam commuting (berangkat dan pulang kerja/sekolah).

Dari pola ini, layanan bike-sharing dapat dioptimalkan dengan:
- Meningkatkan jumlah sepeda yang tersedia pada jam-jam sibuk untuk mengakomodasi tingginya permintaan.
- Menyediakan diskon atau promosi pada jam-jam sepi untuk mendorong lebih banyak penggunaan dan meningkatkan efisiensi layanan.
""")

st.caption('Copyright (c) Dicoding 2025')