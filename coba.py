import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse 
import seaborn as sns
from sklearn.metrics import mean_squared_error
import matplotlib.ticker as mticker

# === CONFIG STREAMLIT ===
st.set_page_config(page_title="Dashboard", layout="wide")

# === TITLE DASHBOARD ===
st.markdown(
    """
    <h1 style='text-align: center;'>
        Peramalan Jumlah Wisatawan di Kabupaten/Kota di Provinsi DI Yogyakarta Menggunakan GSTAR-GLS-SVR
    </h1>
    """,
    unsafe_allow_html=True
)

# === LOAD DATA ===
file_path = "rekap svr [36].xlsx"
fitted_df = pd.read_excel(file_path, sheet_name='fitted value', index_col=0)
aktual_df = pd.read_excel(file_path, sheet_name='asli', index_col=0)
ramal_df = pd.read_excel(file_path, sheet_name='forecast', index_col=0)
tanggal_forecast = pd.read_excel(file_path, sheet_name='forecast')[['Bulan-tahun']]

# === DROPDOWN WILAYAH + "Main" ===
daftar_wilayah = {
    "Kulon Progo": "KP",
    "Bantul": "BT",
    "Gunung Kidul": "GK",
    "Sleman": "SL",
    "Kota Yogyakarta": "KY"
}

# Tambahkan opsi "Main" di awal
opsi_dropdown = ["Provinsi DI Yogyakarta"] + list(daftar_wilayah.keys())

# === SELECTBOX WILAYAH ===
wilayah_pilihan = st.selectbox("Pilih Kabupaten/Kota", options=opsi_dropdown)

# === HALAMAN UTAMA ===
if wilayah_pilihan == "Provinsi DI Yogyakarta":
    st.markdown("#### 📍 Profil Provinsi DI Yogyakarta")

    col1, col2 = st.columns([5, 2])

    with col1:
        st.markdown(
            """
            <div style='font-size: 15px; text-align: justify;'>
            <b>Fakta Singkat:</b><br>
            • Terdiri dari 5 kabupaten/kota yakni Kabupaten Kulon Progo, Kabupaten Bantul, Kabupaten Gunung Kidul, Kabupaten Sleman, dan Kota Yogyakarta.<br>
            • Salah satu Destinasi Pariwisata Nasional (DPN) dengan ikon nasional Keraton Yogyakarta.<br>
            • Terkenal dengan warisan budaya, wisata alam, dan kuliner khas.<br>
            • Kontribusi sektor pariwisata terhadap PDRB Provinsi DIY tahun 2023 naik 8,76% dibandingkan tahun sebelumnya.<br>
            • PAD Provinsi DI Yogyakarta dari sektor pariwisata mencapai Rp 792.049.186.414, atau meningkat sebesar 105,7% dibandingkan tahun 2022.<br>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='font-size: 15px; text-align: justify;'>
            <b>Destinasi Wisata Populer:</b><br>
            • <b>Kulon Progo</b>: 
            <a href="https://www.google.com/maps?q=Kalibiru" target="_blank">Kalibiru</a>,
            <a href="https://www.google.com/maps?q=Pule+Payung" target="_blank">Pule Payung</a>,<br> 
            • <b>Bantul</b>: 
            <a href="https://www.google.com/maps?q=Pantai+Parangtritis" target="_blank">Pantai Parangtritis</a>, 
            <a href="https://www.google.com/maps?q=Gumuk+Pasir" target="_blank">Gumuk Pasir</a><br>
            • <b>Gunung Kidul</b>: 
            <a href="https://www.google.com/maps?q=Goa+Pindul" target="_blank">Goa Pindul</a>,
            <a href="https://www.google.com/maps?q=Pantai+Indrayanti" target="_blank">Pantai Indrayanti</a><br> 
            • <b>Sleman</b>: 
            <a href="https://www.google.com/maps?q=Candi+Prambanan" target="_blank">Candi Prambanan</a>, 
            <a href="https://www.google.com/maps?q=Tebing+Breksi" target="_blank">Tebing Breksi</a><br>
            • <b>Kota Yogyakarta</b>: 
            <a href="https://www.google.com/maps?q=Malioboro" target="_blank">Malioboro</a>, 
            <a href="https://www.google.com/maps?q=Keraton+Yogyakarta" target="_blank">Keraton Yogyakarta</a><br>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("---")  # Garis pembatas agar tidak terlalu mepet

    import streamlit as st
    import folium
    from streamlit_folium import st_folium
    from folium.features import GeoJsonTooltip
    import json
    import pandas as pd

    # === Load Data ===
    file_path = "rekap svr [36].xlsx"
    aktual_df = pd.read_excel(file_path, sheet_name='asli', index_col=0)
    forecast_df = pd.read_excel(file_path, sheet_name='forecast', index_col=0)

    # === Rename Forecast Columns ===
    kode_ke_nama = {
        "KP": "Kabupaten Kulon Progo",
        "BT": "Kabupaten Bantul",
        "GK": "Kabupaten Gunung Kidul",
        "SL": "Kabupaten Sleman",
        "KY": "Kota Yogyakarta"
    }
    forecast_df = forecast_df.rename(columns=kode_ke_nama)

    # Pastikan index datetime
    aktual_df.index = pd.to_datetime(aktual_df.index)
    forecast_df.index = pd.to_datetime(forecast_df.index)

    # Rename aktual_df kolom
    aktual_df = aktual_df.rename(columns=kode_ke_nama)

    # === Gabungkan Data Per Tahun ===
    total_wisatawan_per_tahun = {}

    # Tahun 2023 (aktual)
    data_2023 = aktual_df[aktual_df.index.year == 2023]
    total_2023 = data_2023.sum()
    total_wisatawan_per_tahun[2023] = total_2023.to_dict()

    # Tahun 2024–2026 (forecast)
    for tahun in [2024, 2025, 2026]:
        data_forecast = forecast_df[forecast_df.index.year == tahun]
        total = data_forecast.sum()
        total_wisatawan_per_tahun[tahun] = total.to_dict()

    # === Load GeoJSON ===
    with open("batas_diy.geojson", "r") as f:
        geojson_diy = json.load(f)

    # === Warna Tetap per Wilayah ===
    warna_per_wilayah = {
        "Kabupaten Kulon Progo": "#F9D923",
        "Kabupaten Bantul": "#3C84AB",
        "Kabupaten Gunung Kidul": "#A2C579",
        "Kabupaten Sleman": "#FF7F50",
        "Kota Yogyakarta": "#9D4EDD"
    }

    # === Dropdown Pilihan Tahun (DIPINDAHKAN KE ATAS) ===
    st.markdown("### 📌 Peta dan Statistik Deskriptif")
    tahun_pilihan = st.selectbox(
        "Pilih Tahun", 
        options=[2023, 2024, 2025, 2026], 
        index=0,
        format_func=lambda x: f"Tahun {x}" if x == 2023 else f"Peramalan Tahun {x}"
    )

    # === Bagi jadi dua kolom ===
    col1, col2 = st.columns([1, 1])

    with col1:
        with st.container():
            judul_peta = (
                f"### 🗺️ Peta Informasi Jumlah Wisatawan Tahun {tahun_pilihan}" 
                if tahun_pilihan == 2023 
                else f"### 🗺️ Peta Informasi Peramalan Jumlah Wisatawan Tahun {tahun_pilihan}"
            )
            st.markdown(judul_peta)
            
            # Ambil data jumlah wisatawan sesuai tahun
            jumlah_dict = total_wisatawan_per_tahun[tahun_pilihan]

            # Tambahkan jumlah ke GeoJSON (dengan format ribuan)
            for feature in geojson_diy["features"]:
                wilayah = feature["properties"]["name"]
                jumlah = jumlah_dict.get(wilayah, 0)
                feature["properties"]["wisatawan"] = f"{jumlah:,.0f}".replace(",", ".")

            # === Buat Peta ===
            m = folium.Map(location=[-7.8, 110.4], zoom_start=10, tiles="cartodbpositron")

            # Tambahkan wilayah dengan warna tetap dan tooltip
            for feature in geojson_diy["features"]:
                wilayah = feature["properties"]["name"]
                warna = warna_per_wilayah.get(wilayah, "#CCCCCC")
                
                folium.GeoJson(
                    feature,
                    name=wilayah,
                    style_function=lambda feature, warna=warna: {
                        "fillColor": warna,
                        "color": "black",
                        "weight": 1.5,
                        "fillOpacity": 0.7
                    },
                    tooltip=GeoJsonTooltip(
                        fields=["name", "wisatawan"],
                        aliases=["Wilayah:", "Wisatawan:"],
                        localize=True,
                        sticky=False,
                        labels=False,
                        style="font-size:10px;",
                        max_width=200
                    )
                ).add_to(m)

            # Tampilkan di Streamlit
            st_folium(m, width=725, height=750, returned_objects=[])
                
     
    with col2:
        with st.container():
            judul_stat = (
                f"### 📊 Statistik Deskriptif Jumlah Wisatawan {tahun_pilihan}" 
                if tahun_pilihan == 2023 
                else f"### 📊 Statistik Deskriptif Peramalan Jumlah Wisatawan Tahun {tahun_pilihan}"
            )
            st.markdown(judul_stat)

            st.markdown(" ")
            # Ambil data tahun yang dipilih
            if tahun_pilihan == 2023:
                df_tahun = aktual_df[aktual_df.index.year == 2023]
            else:
                df_tahun = forecast_df[forecast_df.index.year == tahun_pilihan]

            # Agregasi total per wilayah
            total_per_wilayah = df_tahun.sum()

            total_all = total_per_wilayah.sum()
            rata2 = total_per_wilayah.mean()
            wilayah_max = total_per_wilayah.idxmax()
            nilai_max = total_per_wilayah.max()
            wilayah_min = total_per_wilayah.idxmin()
            nilai_min = total_per_wilayah.min()

            # Format ribuan
            total_all_str = f"{total_all:,.0f}".replace(",", ".")
            rata2_str = f"{rata2:,.0f}".replace(",", ".")
            nilai_max_str = f"{nilai_max:,.0f}".replace(",", ".")
            nilai_min_str = f"{nilai_min:,.0f}".replace(",", ".")

            # Buat DataFrame untuk tabel
            deskriptif_df = pd.DataFrame({
                "Statistik": ["Total", "Rata-rata", "Maksimum", "Minimum"],
                "Nilai": [
                    f"{total_all_str} wisatawan",
                    f"{rata2_str} wisatawan",
                    f"{nilai_max_str} wisatawan di {wilayah_max}",
                    f"{nilai_min_str} wisatawan di {wilayah_min}"
                ]
            })

            st.dataframe(deskriptif_df, hide_index=True, use_container_width=True)

            st.markdown(
                f"""
                <div style="background-color: #dbe9f4; padding: 10px; border-radius: 5px; text-align: center;">
                    <p style="font-size: 14px;">
                        Tabel statistik deskriptif menampilkan ringkasan jumlah wisatawan dari keseluruhan data yang diamati. 
                        Informasi ini memberikan gambaran awal mengenai sebaran jumlah kunjungan wisatawan yang tercatat dalam data. 
                        Total wisatawan yang tercatat mencapai <b>{total_all_str}</b> wisatawan. 
                        Secara rata-rata, terdapat <b>{rata2_str}</b> wisatawan yang berkunjung setiap bulan. 
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


            # === CORRELATION HEATMAP ===
            judul_kor = (
                f"### 🔄 Korelasi Jumlah Wisatawan Antar Wilayah Tahun {tahun_pilihan}" 
                if tahun_pilihan == 2023 
                else f"### 🔄 Korelasi Peramalan Jumlah Wisatawan Antar Wilayah Tahun {tahun_pilihan}"
            )
            st.markdown(judul_kor)

            # Ambil data tahun untuk korelasi
            if tahun_pilihan == 2023:
                df_corr = aktual_df[aktual_df.index.year == 2023]
            else:
                df_corr = forecast_df[forecast_df.index.year == tahun_pilihan]

            # Korelasi hanya numerik
            corr = df_corr.corr()

            # Buat heatmap
            fig, ax = plt.subplots(figsize=(2.8, 2.8), dpi=100)
            sns.heatmap(
                corr,
                annot=True,
                fmt=".2f",
                cmap="coolwarm",
                vmin=-1,
                vmax=1,
                linewidths=0.4,
                square=False,
                ax=ax,
                cbar=False,
                annot_kws={"size": 5}
            )

            # Label sumbu X dan Y kecil dan miring
            ax.set_xticklabels(ax.get_xticklabels(), fontsize=4, rotation=45, ha='right')
            ax.set_yticklabels(ax.get_yticklabels(), fontsize=4, rotation=0)
            #ax.set_title(f"Korelasi Antar Wilayah Tahun {tahun_pilihan}", fontsize=7, pad=5)

            plt.tight_layout()

            # === Tampilkan plot TANPA memenuhi lebar kontainer ===
            st.pyplot(fig, use_container_width=False)

    #BOXPLOT MUSIMAN
    # === BOX PLOT POLA MUSIMAN ===
    st.markdown("---")  # Garis pembatas agar tidak terlalu mepet
    st.markdown("### 📦 Pola Musiman Jumlah Wisatawan")

    # Salin data dan olah
    df_aktual = aktual_df.copy()
    df_aktual.index = pd.to_datetime(df_aktual.index)
    df_aktual["Bulan"] = df_aktual.index.month
    df_aktual["Total"] = df_aktual.drop(columns=["Bulan"], errors='ignore').sum(axis=1)

    # Siapkan untuk boxplot
    import calendar
    boxplot_df = df_aktual[["Bulan", "Total"]].copy()
    boxplot_df["Bulan"] = boxplot_df["Bulan"].apply(lambda x: calendar.month_name[x])
    bulan_order = list(calendar.month_name)[1:]

    # Buat boxplot musiman
    fig, ax = plt.subplots(figsize=(10, 4.2))
    sns.boxplot(data=boxplot_df, x="Bulan", y="Total", order=bulan_order, palette="pastel", ax=ax)

    ax.set_title("Distribusi Jumlah Wisatawan per Bulan (Seluruh Kab/Kota di Provinsi DIY 2010–2023)", fontsize=10)
    ax.set_xlabel("Bulan", fontsize=5)
    ax.set_ylabel("Jumlah Wisatawan", fontsize=5)
    ax.tick_params(axis='x', labelsize=6, rotation=45)
    ax.tick_params(axis='y', labelsize=6)
    ax.grid(True, linestyle='--', linewidth=0.5)

    st.pyplot(fig)
    st.markdown(
        f"""
        <div style="background-color: #dbe9f4; padding: 10px; border-radius: 5px; text-align: center;">
            Plot ini menunjukkan pola musiman jumlah wisatawan dari tahun 2010 hingga 2023. 
            Terlihat adanya lonjakan pada Bulan <b>Desember</b> hal ini dikarenakan bertepatan dengan
            <b>libur akhir tahun, libur natal, dan libur sekolah</b>
        </div>
        """,
        unsafe_allow_html=True
    )



#--------------------------------------------------------------------------------------------------------------------------------------------------------------


# === HALAMAN WILAYAH ===
else:
    kolom = daftar_wilayah[wilayah_pilihan]
    st.subheader(f"📊 Hasil Peramalan: {wilayah_pilihan}")

    # Ambil data berdasarkan wilayah yang dipilih
    fitted = fitted_df[[kolom]]
    aktual = aktual_df[[kolom]]
    ramal = ramal_df[[kolom]]

    # Atur index ramal sebagai tanggal forecast
    forecast_index = tanggal_forecast.iloc[-len(ramal):]['Bulan-tahun']
    ramal.index = forecast_index

    # Pastikan index dalam format datetime
    aktual.index = pd.to_datetime(aktual.index)
    ramal.index = pd.to_datetime(ramal.index)

    # === PLOT UTAMA (GARIS) ===
    fig, ax = plt.subplots(figsize=(8, 3.5))  # Ukuran lebih kecil dan lebar
    ax.plot(aktual, label='Data Aktual', color='blue', linewidth=1.5)
    ax.plot(fitted, linestyle='--', color='orange', label='Model Fitting', linewidth=1.5)
    ax.plot(ramal, label='Forecast', color='red', linestyle='--', linewidth=1.5)

    # Garis vertikal pemisah forecast
    tanggal_mulai_forecast = ramal.index[0]
    ax.axvline(x=tanggal_mulai_forecast, color='black', linestyle=':', linewidth=1)

    # Atur x-ticks tahunan
    all_dates = pd.date_range(start=aktual.index.min(), end=ramal.index.max(), freq='YS')
    years = [pd.to_datetime(str(date.year)) for date in all_dates]

    ax.set_xticks(years)
    ax.set_xticklabels([str(date.year) for date in years], fontsize=6, rotation=45)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x/1000):,}'.replace(',', '.')))


    ax.set_title(f"Peramalan Hybrid Jumlah Wisatawan - {wilayah_pilihan}", fontsize=10)
    ax.set_xlabel("Tahun", fontsize=6)
    ax.set_ylabel("Jumlah Wisatawan (ribu)", fontsize=6)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.legend(fontsize=6)
    ax.grid(True, linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # === HITUNG DAN TAMPILKAN NILAI RMSE FITTED vs AKTUAL ===
    # === Nilai RMSE per wilayah ===
    rmse_dict = {
        "Kulon Progo": "47.688",
        "Bantul": "167.138",
        "Gunung Kidul": "145.132",
        "Sleman": "178.445",
        "Kota Yogyakarta": "149.360"
    }

    # Ambil nilai RMSE berdasarkan wilayah
    rmse_str = rmse_dict.get(wilayah_pilihan, "-")

    # Tampilkan dengan markdown
    st.markdown(
        f"""
        <div style="background-color: #dbe9f4; padding: 10px; border-radius: 5px; text-align: center;font-size: 18px;">
            <b>Nilai RMSE</b> antara data asli dan <i>model fitted</i> menggunakan GSTAR-GLS-SVR pada periode <i>testing</i> untuk wilayah <b>{wilayah_pilihan}</b> adalah <b>{rmse_str}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")  # Garis pembatas agar tidak terlalu mepet

    # === TABEL HASIL PERAMALAN DENGAN PENANDA NILAI TERTINGGI ===



    # === LAYOUT 2 KOLOM: TABEL & INTERPRETASI ===
    
    st.markdown("### 📄 Tabel Hasil Peramalan Jumlah Wisatawan dan Interpretasi")

    # Dropdown tahun berada di atas kedua kolom dan membentang penuh
    tahun_tersedia = [2024, 2025, 2026]
    tahun_dipilih = st.selectbox("Pilih Tahun Peramalan", options=tahun_tersedia)

    # Bagi jadi dua kolom
    col1, col2 = st.columns([1, 1])  # Masing-masing setengah halaman

    with col1:
        st.markdown("### 📊 Tabel Jumlah Wisatawan")

        # Siapkan data
        df_ramal_tampil = ramal.copy()
        df_ramal_tampil = df_ramal_tampil.reset_index()
        df_ramal_tampil.columns = ["Tanggal", "Jumlah Wisatawan"]
        df_ramal_tampil["Tahun"] = df_ramal_tampil["Tanggal"].dt.year
        df_ramal_tampil["Bulan"] = df_ramal_tampil["Tanggal"].dt.strftime('%B')

        # Filter berdasarkan tahun yang dipilih
        df_ramal_tampil = df_ramal_tampil[df_ramal_tampil["Tahun"] == tahun_dipilih]

        # Tandai nilai maksimum tahun itu
        if not df_ramal_tampil.empty:
            idx_max = df_ramal_tampil["Jumlah Wisatawan"].idxmax()
            df_ramal_tampil["Keterangan"] = ""
            df_ramal_tampil.loc[idx_max, "Keterangan"] = "📌 Tertinggi"

            # Format angka
            df_ramal_tampil["Jumlah Wisatawan"] = df_ramal_tampil["Jumlah Wisatawan"].apply(lambda x: f"{int(x):,}".replace(",", "."))

            # Urutkan dan tampilkan
            df_ramal_tampil = df_ramal_tampil[["Tahun", "Bulan", "Jumlah Wisatawan", "Keterangan"]]
            st.data_editor(
                df_ramal_tampil,
                hide_index=True,
                use_container_width=True,
                height=280
            )
        else:
            st.info("Tidak ada data untuk tahun ini.")

    with col2:
        judul_inter = (
                f"### 📝 Interpretasi Hasil Peramalan {tahun_dipilih}" 
            )
        st.markdown(judul_inter)
        st.markdown(" ")
        st.markdown(" ")

        if not df_ramal_tampil.empty:
            bulan_tertinggi = df_ramal_tampil.loc[idx_max, "Bulan"]
            jumlah_tertinggi = df_ramal_tampil.loc[idx_max, "Jumlah Wisatawan"]
            total_tahun = df_ramal_tampil["Jumlah Wisatawan"].str.replace(".", "").astype(int).sum()
            total_tahun_str = f"{total_tahun:,}".replace(",", ".")

            st.markdown(
                f"""
                <div style='font-size: 16px; text-align: justify;'>
                Berdasarkan hasil peramalan pada tahun <b>{tahun_dipilih}</b>, jumlah wisatawan diperkirakan mencapai 
                <b>{total_tahun_str}</b> wisatawan. Hal ini menunjukkan adanya tren pemulihan dan peningkatan minat perjalanan setelah pandemi COVID-19,
                yang sesuai dengan fenomena <i>revenge tourism</i>.<br><br>

                Jumlah wisatawan terbanyak diperkirakan terjadi pada bulan <b>{bulan_tertinggi}</b> dengan jumlah sekitar <b>{jumlah_tertinggi}</b> wisatawan. 
                Peningkatan ini kemungkinan disebabkan oleh periode musim liburan, seperti libur sekolah, Natal, atau tahun baru, 
                yang biasanya mendorong mobilitas masyarakat untuk berwisata, terutama ke destinasi populer di wilayah ini. Pola lonjakan jumlah wisatawan pada bulan <b>{bulan_tertinggi}</b>
                menunjukkan tren musiman yang sama dengan tahun sebelumnya.
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Interpretasi tidak tersedia karena tidak ada data untuk tahun ini.")
