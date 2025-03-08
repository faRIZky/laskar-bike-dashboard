import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard")

# Set tema visual
sns.set_theme(style="whitegrid")

# Load data
bike_df = pd.read_csv("bike.csv")

# Fungsi untuk menghitung rata-rata pengguna terdaftar dan tidak terdaftar
def create_avg_registered_df(df):
    avg_registered_df = df.groupby('year')['registered'].mean()
    return avg_registered_df

def create_avg_unregistered_df(df):
    avg_unregistered_df = df.groupby('year')['unregistered'].mean()
    return avg_unregistered_df

# DataFrame rata-rata
avg_registered_df = create_avg_registered_df(bike_df)
avg_unregistered_df = create_avg_unregistered_df(bike_df)

# Sidebar
with st.sidebar:
    st.title("🚴 Bike Sharing Dashboard")
    st.markdown(
        """
        **Fitur Dashboard:**
        - Rata-rata peminjaman per musim
        - Perbandingan pengguna terdaftar dan tidak terdaftar
        - Distribusi peminjaman pada hari kerja & libur
        - Clustering peminjaman berdasarkan jam
        """
    )
    st.info("Gunakan fitur interaktif untuk eksplorasi lebih lanjut!")

# Header utama
title_col, _ = st.columns([3, 1])
with title_col:
    st.title("Bike Sharing Dashboard 🚲")

# Warna untuk musim
season_colors = ['#76c7c0', '#ffcc5c', '#ff6f61', '#6b5b95']

# Bar chart: Rata-rata peminjaman berdasarkan musim
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
    st.write(
        """
        Total rata-rata permintaan peminjaman pada tahun 2021 lebih tinggi. Hal ini juga sebanding lurus dengan naiknya jumlah permintaan dari pengguna unregistered sebesar 48.28%. Walaupun begitu, gap nilai registered dan unregistered sangatlah jauh. Angka unregistered tidak menyentuh angka 100 pada tahun 2020 dan 2021.
    """
    )

# Perbandingan peminjaman pengguna terdaftar dan tidak terdaftar
st.subheader("Bagaimana rata-rata peminjaman sepeda pada hari kerja dan hari libur?")
tabs = st.tabs(["Registered Users", "Unregistered Users"])

with tabs[0]:
    st.subheader("Registered Users per Year")
    fig_registered, ax_registered = plt.subplots(figsize=(8, 6))
    ax_registered.bar(avg_registered_df.index, avg_registered_df.values, color='#2AAA8A')
    ax_registered.set_title('Mean Bike Rental Count by Registered Users')
    ax_registered.set_xlabel('Year')
    ax_registered.set_ylabel('Average Registered')
    ax_registered.set_xticks([0, 1])
    ax_registered.set_xticklabels(['2020', '2021'])
    st.pyplot(fig_registered)


with tabs[1]:
    st.subheader("Unregistered Users per Year")
    fig_unregistered, ax_unregistered = plt.subplots(figsize=(8, 6))
    ax_unregistered.bar(avg_unregistered_df.index, avg_unregistered_df.values, color='#FF6F61')
    ax_unregistered.set_title('Mean Bike Rental Count by Unregistered Users')
    ax_unregistered.set_xlabel('Year')
    ax_unregistered.set_ylabel('Average Unregistered')
    ax_unregistered.set_xticks([0, 1])
    ax_unregistered.set_xticklabels(['2020', '2021'])
    st.pyplot(fig_unregistered)

with st.expander("Lihat penjelasan"):
    st.write(
        """
        Rata-rata permintaan peminjaman pada tahun 2021 lebih tinggi dibandingkan 2020.
        """
    )

# Pie Chart: Distribusi peminjaman pada hari kerja dan hari libur
st.subheader("Bagaimana distribusi permintaan peminjaman sepeda pada hari kerja dan hari libur?")
tabs = st.tabs(["Working Day", "Holiday"])

# Nama hari dalam seminggu
weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Data untuk hari kerja dan libur
weekday_counts_0 = bike_df[bike_df['holiday'] == 0].groupby('weekday').size()
weekday_counts_1 = bike_df[bike_df['holiday'] == 1].groupby('weekday').size()

with tabs[0]:
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.pie(weekday_counts_0, labels=[weekday_names[idx] for idx in weekday_counts_0.index], autopct='%1.1f%%')
    ax1.set_title('Weekday Distribution for Working Days')
    st.pyplot(fig1)

with tabs[1]:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.pie(weekday_counts_1, labels=[weekday_names[idx] for idx in weekday_counts_1.index], autopct='%1.1f%%')
    ax2.set_title('Weekday Distribution for Holidays')
    st.pyplot(fig2)

with st.expander("Lihat penjelasan"):
    st.write(
        """
    Permintaan cenderung merata pada hari kerja, tetapi meningkat secara signifikan pada hari libur, terutama pada hari Selasa dengan presentase sebesar 71.4%. Kemungkinan pada hari kerja, sebagian penduduk menggunakan penyewaan sepeda dan menyewa sepeda sudah menjadi suatu hal yang mereka lakukan sehari-hari kerja.
    """
    )

# Clustering berdasarkan jam peminjaman
st.subheader("Bagaimana pola peminjaman berdasarkan jam dengan clustering?")

def categorize_hour(hour):
    if 0 <= hour <= 6:
        return "Low Usage"
    elif 7 <= hour <= 16:
        return "Medium Usage"
    else:
        return "High Usage"

bike_df["Usage Category"] = bike_df["hour"].apply(categorize_hour)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="Usage Category", y="count", data=bike_df, palette=["#6495ED", "#D3D3D3", "#FF6F61"])
ax.set_xlabel("Usage Category")
ax.set_ylabel("Bike Rental Count")
ax.set_title("Clustering of Bike Rentals by Hour (Without ML)")
st.pyplot(fig)

with st.expander("Lihat penjelasan"):
    st.write(
        """
         Dari hasil analisis clustering manual terhadap jumlah peminjaman sepeda berdasarkan jam, dapat disimpulkan bahwa terdapat tiga kategori utama dalam pola peminjaman:

- Low Usage (Jam 0-6) Pada periode ini, jumlah peminjaman sepeda sangat rendah, dengan sebagian besar peminjaman berada di bawah 100 unit. Hal ini wajar mengingat rentang waktu ini merupakan waktu istirahat malam hingga dini hari, di mana aktivitas luar ruangan minim.

- Medium Usage (Jam 7-16) Pada pagi hingga sore hari, jumlah peminjaman meningkat secara signifikan. Rentang peminjaman lebih luas dibandingkan dengan periode sebelumnya, menunjukkan bahwa sepeda digunakan untuk berbagai keperluan seperti transportasi ke kantor, sekolah, atau aktivitas siang hari lainnya.

- High Usage (Jam 17-23) Jumlah peminjaman sepeda mencapai puncaknya pada sore hingga malam hari. Banyak peminjaman yang melebihi 400 unit, yang mengindikasikan bahwa sepeda banyak digunakan untuk perjalanan pulang kerja, rekreasi, atau aktivitas santai di malam hari.

Jam sore hingga malam merupakan waktu dengan permintaan tertinggi, sehingga penyedia layanan sepeda dapat mempertimbangkan peningkatan ketersediaan unit pada periode ini. Dini hari memiliki peminjaman terendah, sehingga jumlah sepeda yang tersedia bisa dikurangi untuk efisiensi.
    """
    )

st.caption('© Dicoding 2025')
