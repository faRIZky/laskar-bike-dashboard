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

# Konversi kolom tanggal
bike_df["datetimes"] = pd.to_datetime(bike_df["datetimes"])
bike_df["date"] = bike_df["datetimes"].dt.date  # Tambahkan kolom date agar bisa difilter

# Mapping nama musim (season)
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
bike_df["season"] = bike_df["season"].map(season_mapping)

# Mapping kondisi cuaca (weathersituation)
weather_mapping = {
    1: "Clear, Few clouds, Partly cloudy",
    2: "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
    3: "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
    4: "Heavy Rain + Ice Pellets + Thunderstorm + Mist, Snow + Fog"
}
bike_df["weathersituation"] = bike_df["weathersituation"].map(weather_mapping)

weekday_mapping = {0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"}
bike_df["weekday"] = bike_df["weekday"].map(weekday_mapping)

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
        - **Filter berdasarkan tanggal, musim, dan cuaca**
        """
    )
    st.info("Gunakan fitur interaktif untuk eksplorasi lebih lanjut!")

    # Filter berdasarkan tanggal
    start_date = st.date_input("Pilih tanggal mulai", bike_df["date"].min())
    end_date = st.date_input("Pilih tanggal akhir", bike_df["date"].max())

    # Filter berdasarkan musim dan cuaca
    season_filter = st.multiselect("Pilih musim", options=bike_df["season"].unique(), default=bike_df["season"].unique())
    weather_filter = st.multiselect("Pilih kondisi cuaca", options=bike_df["weathersituation"].unique(),
                                    default=bike_df["weathersituation"].unique())

# Terapkan filter
filtered_df = bike_df[
    (bike_df["date"] >= start_date) &
    (bike_df["date"] <= end_date) &
    (bike_df["season"].isin(season_filter)) &
    (bike_df["weathersituation"].isin(weather_filter))
]

# Header utama
st.title("Bike Sharing Dashboard 🚲")

# Bar chart: Rata-rata peminjaman berdasarkan musim
st.subheader("Bagaimana rata-rata peminjaman pada setiap musim?")
avg_season_df = filtered_df.groupby("season")["count"].mean()

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(avg_season_df.index, avg_season_df.values, color=['#76c7c0', '#ffcc5c', '#ff6f61', '#6b5b95'])
ax.set_xticklabels(avg_season_df.index, rotation=30)
ax.set_title("Mean Bike Rental Count by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Average Rental Count")
st.pyplot(fig)

# Perbandingan peminjaman pengguna terdaftar dan tidak terdaftar
st.subheader("Bagaimana perbandingan peminjaman pengguna terdaftar dan tidak terdaftar?")
avg_registered_df = filtered_df.groupby("year")["registered"].mean()
avg_unregistered_df = filtered_df.groupby("year")["unregistered"].mean()

tabs = st.tabs(["Registered Users", "Unregistered Users"])
with tabs[0]:
    fig_registered, ax_registered = plt.subplots(figsize=(8, 6))
    ax_registered.bar(avg_registered_df.index, avg_registered_df.values, color='#2AAA8A')
    ax_registered.set_title("Mean Bike Rental Count by Registered Users")
    ax_registered.set_xlabel("Year")
    ax_registered.set_ylabel("Average Registered")
    ax_registered.set_xticks([0, 1])
    ax_registered.set_xticklabels(['2011', '2012'])
    st.pyplot(fig_registered)

with tabs[1]:
    fig_unregistered, ax_unregistered = plt.subplots(figsize=(8, 6))
    ax_unregistered.bar(avg_unregistered_df.index, avg_unregistered_df.values, color='#FF6F61')
    ax_unregistered.set_title("Mean Bike Rental Count by Unregistered Users")
    ax_unregistered.set_xlabel("Year")
    ax_unregistered.set_ylabel("Average Unregistered")
    ax_unregistered.set_xticks([0, 1])
    ax_unregistered.set_xticklabels(['2011', '2012'])
    st.pyplot(fig_unregistered)

# Pie Chart: Distribusi peminjaman pada hari kerja dan hari libur
st.subheader("Bagaimana distribusi permintaan peminjaman sepeda pada hari kerja dan hari libur?")
tabs = st.tabs(["Working Day", "Holiday"])

weekday_counts_0 = filtered_df[filtered_df["holiday"] == 0].groupby("weekday")["count"].count()
weekday_counts_1 = filtered_df[filtered_df["holiday"] == 1].groupby("weekday")["count"].count()

with tabs[0]:
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    ax1.pie(weekday_counts_0, labels=weekday_counts_0.index, autopct="%1.1f%%")
    ax1.set_title("Distribusi Peminjaman pada Hari Kerja")
    st.pyplot(fig1)

with tabs[1]:
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    ax2.pie(weekday_counts_1, labels=weekday_counts_1.index, autopct="%1.1f%%")
    ax2.set_title("Distribusi Peminjaman pada Hari Libur")
    st.pyplot(fig2)


# Clustering berdasarkan jam peminjaman
st.subheader("Bagaimana pola peminjaman berdasarkan jam dengan clustering?")

def categorize_hour(hour):
    if 0 <= hour <= 6:
        return "Low Usage"
    elif 7 <= hour <= 16:
        return "Medium Usage"
    else:
        return "High Usage"

filtered_df.loc[:, "Usage Category"] = filtered_df["hour"].apply(categorize_hour)

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x="Usage Category", y="count", data=filtered_df, palette=["#6495ED", "#D3D3D3", "#FF6F61"])
ax.set_xlabel("Usage Category")
ax.set_ylabel("Bike Rental Count")
ax.set_title("Clustering of Bike Rentals by Hour (Without ML)")
st.pyplot(fig)

with st.expander("See explanation"):
    st.write(
    """
    Clustering ini dilakukan secara **rule-based** berdasarkan pola peminjaman sepeda pada berbagai jam dalam sehari.  
    Kategori ini membagi aktivitas peminjaman menjadi **tiga kelompok utama** berdasarkan kepadatan peminjaman sepeda:

    - **Low Usage (00:00 - 06:00)**  
      Pada rentang ini, jumlah peminjaman cenderung rendah. Biasanya digunakan untuk keperluan **darurat, perjalanan malam, atau event khusus**.  
      Aktivitas umum: pekerja shift malam, pengantar barang, atau individu yang bepergian pada jam sepi.

    - **Medium Usage (07:00 - 16:00)**  
      Periode ini adalah **jam sibuk utama** di mana banyak orang menggunakan sepeda untuk **pergi ke kantor, sekolah, atau aktivitas sehari-hari**.  
      Aktivitas umum: pekerja kantoran, mahasiswa, dan pengguna reguler transportasi umum yang menggunakan sepeda sebagai moda tambahan.

    - **High Usage (17:00 - 23:00)**  
      Puncak penggunaan sepeda sering terjadi setelah jam kerja. Banyak orang yang menggunakan sepeda untuk **pulang kerja, rekreasi, atau aktivitas sosial**.  
      Aktivitas umum: commuting pulang kantor, olahraga sore, dan perjalanan ke tempat hiburan atau restoran.
    """
    )
st.caption("© Dicoding 2025")
