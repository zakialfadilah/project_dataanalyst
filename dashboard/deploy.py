import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
data_customers = pd.read_csv("dashboard/customers_dataset.csv")
data_order = pd.read_csv("dashboard/data_order_cleaned.csv")

st.write("""
    # Visualisasi Data Analysis E-Commerce
""")

st.subheader('Pertanyaan & Tujuan Analisis')
st.write("""
   1. Negara mana yang memiliki potensi pertumbuhan e-commerce tertinggi berdasarkan total customers dan layak untuk dijadikan prioritas ekspansi layanan?
   2. Bagaimana perkembangan penjualan pada e-commerce dalam tahun 2017 dan 2018? dan bagaimana tren yang terjadi perbulannya?
""")

tab1, tab2 = st.tabs(["Geographic Analysis", "Sales Quantity Growth"])

with tab1:
    st.header("Geographic Analysis")
    

    
    
    customer_counts = (
        data_customers.groupby("customer_state")["customer_id"]
        .count()
        .reset_index()
        .rename(columns={"customer_state": "State", "customer_id": "Total Customers"})
        .sort_values(by="Total Customers", ascending=False)
    )
    
    st.write("Berikut merupakan Total customer terbesar hingga terkecil di Negara yang sama")
    st.dataframe(customer_counts)
    
    state_options = ["All"] + customer_counts["State"].unique().tolist()
    selected_state = st.selectbox("Pilih State untuk visualisasi", state_options)
    
    if selected_state != "All":
        filtered_data = customer_counts[customer_counts["State"] == selected_state]
        st.write(f"Total customers dari negara {selected_state} adalah {filtered_data['Total Customers'].values[0]}")
    else:
        filtered_data = customer_counts
    
    plt.figure(figsize=(10, 6))
    plt.bar(filtered_data["State"], filtered_data["Total Customers"], color="green")
    plt.title("Total Customers per State", fontsize=14)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Total Customers", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(plt)
    
    st.subheader("Kategori Customer Berdasarkan State")
    def categorize_customers(total):
        if total > 500:
            return "High"
        elif total >= 100:
            return "Medium"
        else:
            return "Low"
    
    customer_counts["Category"] = customer_counts["Total Customers"].apply(categorize_customers)
    
    category_options = ["All"] + customer_counts["Category"].unique().tolist()
    selected_category = st.selectbox("Pilih Kategori Customer", category_options)
    
    if selected_category != "All":
        filtered_category_data = customer_counts[customer_counts["Category"] == selected_category]
    else:
        filtered_category_data = customer_counts
    
    st.dataframe(filtered_category_data)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x="State", y="Total Customers", hue="Category", data=filtered_category_data, palette={"High": "green", "Medium": "orange", "Low": "red"})
    plt.title("Customer Categories per State", fontsize=14)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Total Customers", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(plt)

with tab2:
    st.header("Sales Quantity Growth")
    
    data_order['order_purchase_timestamp'] = pd.to_datetime(data_order['order_purchase_timestamp'])
    data_order['year'] = data_order['order_purchase_timestamp'].dt.year
    data_order['month'] = data_order['order_purchase_timestamp'].dt.month
    
    customer_count_per_year = data_order.groupby('year')['customer_id'].nunique()
    total_sales_per_month_year = data_order.groupby(['year', 'month'])['order_id'].count()
    
    st.write("Jumlah pelanggan unik per tahun:")
    st.dataframe(customer_count_per_year)
    st.write("Total pembelian tiap bulan per tahun:")
    st.dataframe(total_sales_per_month_year)
    
    year_options = data_order['year'].unique().tolist()
    selected_year = st.selectbox("Pilih Tahun untuk visualisasi", year_options)
    
    filtered_sales = data_order[data_order['year'] == selected_year]
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_sales.groupby(['year', 'month'])['order_id'].count().reset_index(),
                 x='month', y='order_id', marker='o')
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah Pesanan")
    plt.title(f"Tren Penjualan Tahun {selected_year}")
    plt.xticks(range(1, 13))
    plt.ylim(0)
    st.pyplot(plt)
