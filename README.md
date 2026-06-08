# 📦 UAS Data Warehouse — Olist Brazilian E-Commerce

<p align="center">
  <img src="https://img.shields.io/badge/status-selesai-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/dataset-Olist%20Brazilian%20E--Commerce-blue" alt="Dataset">
  <img src="https://img.shields.io/badge/tools-Python%20%7C%20MySQL%20%7C%20Pentaho-orange" alt="Tools">
  <img src="https://img.shields.io/badge/schema-Star%20Schema-ff69b4" alt="Schema">
</p>

---

## 📖 Cerita Dataset: Perjalanan Sebuah Pesanan

> *Di sebuah kota di Brasil, seorang ibu rumah tangga bernama **Ana** sedang duduk di rumahnya di **Sao Paulo**. Ia membuka laptop dan mengunjungi **Olist Marketplace** — sebuah platform e-commerce yang menghubungkan ribuan penjual kecil dengan jutaan pelanggan di seluruh Brasil.*

### 🧑‍🤝‍🧑 Bab 1: Pelanggan

*Ana sudah menjadi pelanggan setia Olist. Data dirinya tersimpan rapi di dalam sistem.*

| Di dataset | Namanya |
|------------|---------|
| `olist_customers_dataset` | `customer_id = "06b8999e..."` |
| | `customer_unique_id = "861eff47..."` |
| | `customer_city = "franca"` |
| | `customer_state = "SP"` |

Ana tinggal di kota Franca, negara bagian **São Paulo (SP)** — daerah dengan aktivitas e-commerce tertinggi di Brasil. Setiap pelanggan memiliki **ID unik** yang tidak akan berubah meskipun mereka mengganti akun. Kode pos mereka (contoh: `14409`) bisa digunakan untuk melihat peta geografis persebaran pelanggan.

### 🛍️ Bab 2: Produk

*Ana mencari hadiah ulang tahun untuk adiknya. Setelah scrolling beberapa saat, matanya tertuju pada sebuah produk.*

```
Produk:  Parfum Wanita "Flor de Liz"
Kategori:  perfumaria (health_beauty)
Berat:  225 gram
Dimensi:  16 x 10 x 14 cm
Harga:  Rp 58,90 BRL
```

| Di dataset | Namanya |
|------------|---------|
| `olist_products_dataset` | `product_id = "4244733e..."` |
| | `product_category_name = "perfumaria"` |
| | `product_weight_g = 225` |
| | `product_length_cm = 16` |

Setiap produk di Olist terdaftar dengan dimensi dan berat — informasi penting untuk menghitung ongkos kirim. Nama kategori masih dalam **Bahasa Portugis** (`perfumaria`), sehingga ada tabel penerjemah:

| `product_category_name_translation` | |
|-------------------------------------|-|
| `perfumaria` | → `health_beauty` |
| `informatica_acessorios` | → `computers_accessories` |
| `cama_mesa_banho` | → `bed_bath_table` |

### 🏪 Bab 3: Seller (Penjual)

*Produk ini dijual oleh seorang penjual dari Campinas, SP.*

```
Seller ID:  48436dade18ac8b2bce089ec2a041202
Kota:  campinas, SP
Kode Pos:  13023
```

| Di dataset | Namanya |
|------------|---------|
| `olist_sellers_dataset` | `seller_id = "48436dade..."` |

Olist memiliki **3.095 seller** tersebar di berbagai kota Brasil. Sebagian besar seller berada di negara bagian tenggara seperti **SP, RJ, dan MG** — pusat ekonomi Brasil.

### 📋 Bab 4: Pesanan Tercipta

*Ana mengklik "Beli". Sebuah pesanan baru lahir.*

```
Order ID:  00010242fe8c5a6d1ba2dd792cb16214
Status:  delivered
Waktu Beli:  2017-09-19 10:56:33
Disetujui:  2017-09-19 11:07:15
Estimasi Sampai:  2017-10-18
```

| Di dataset | Namanya |
|------------|---------|
| `olist_orders_dataset` | `order_id`, `customer_id` |
| | `order_purchase_timestamp` |
| | `order_delivered_customer_date` |

Setiap pesanan mencatat **perjalanan waktu** yang lengkap:
- 🕐 Kapan pelanggan membeli? → `order_purchase_timestamp`
- ✅ Kapan pembayaran disetujui? → `order_approved_at`
- 🚚 Kapan dikirim ke kurir? → `order_delivered_carrier_date`
- 🏠 Kapan sampai ke pelanggan? → `order_delivered_customer_date`

### 📦 Bab 5: Item Pesanan

*Parfum itu masuk ke dalam keranjang sebagai item pertama.*

```
Order Item ke-1 dari 1 item
Harga Produk:  Rp 58,90
Ongkos Kirim:  Rp 13,29
Batas Pengiriman Seller:  2017-09-19 09:45:35
```

| Di dataset | Namanya |
|------------|---------|
| `olist_order_items_dataset` | `order_id`, `product_id`, `seller_id` |
| | `price = 58.90` |
| | `freight_value = 13.29` |

Tabel inilah yang menjadi **jantung transaksi** — menghubungkan pesanan dengan produk dan seller, lengkap dengan nominal uang yang mengalir.

### 💳 Bab 6: Pembayaran

*Ana membayar menggunakan kartu kredit, 8 kali cicilan.*

```
Metode:  credit_card
Cicilan:  8x
Nilai:  Rp 99,33
```

| Di dataset | Namanya |
|------------|---------|
| `olist_order_payments_dataset` | `order_id` |
| | `payment_type = "credit_card"` |
| | `payment_installments = 8` |

Pembayaran di Olist bervariasi: **kartu kredit (76%)**, **boleto (19%)**, **voucher (4%)**, dan **debit (1%)**. Banyak pelanggan Brasil memilih cicilan hingga 24 bulan!

### ⭐ Bab 7: Ulasan & Rating

*Seminggu kemudian, parfum tiba. Ana senang dan memberi ulasan.*

```
Review Score:  5/5
Komentar:  "Recebi bem antes do prazo estipulado."
           (Terima jauh sebelum batas waktu yang ditentukan.)
Tanggal Review:  2017-10-10
```

| Di dataset | Namanya |
|------------|---------|
| `olist_order_reviews_dataset` | `review_id` |
| | `review_score = 5` |
| | `review_comment_message = "Recebi..."` |

Skor review berkisar **1-5** dan menjadi indikator kepuasan pelanggan yang sangat penting untuk analisis bisnis.

### 📍 Bab 8: Geolokasi

*Di balik layar, sistem melacak koordinat geografis setiap kode pos.*

```
Kode Pos:  14409 → Lat: -23.5456, Lng: -46.6392
Kode Pos:  13023 → Lat: -22.8845, Lng: -47.0562
```

| Di dataset | Namanya |
|------------|---------|
| `olist_geolocation_dataset` | `geolocation_zip_code_prefix` |
| | `geolocation_lat`, `geolocation_lng` |

Tabel ini berisi **1 juta titik koordinat** yang memetakan seluruh wilayah Brasil. Ini memungkinkan analisis geografis seperti: *"Daerah mana yang memiliki rata-rata waktu pengiriman terlama?"* atau *"Apakah pelanggan di daerah tertentu cenderung memberi rating lebih rendah?"*

---

## 🏗️ Dari 9 Tabel Menjadi Star Schema

Data mentah dari 9 tabel CSV ditransformasi melalui proses **ETL (Extract, Transform, Load)** menjadi **Star Schema** yang siap analisis.

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUMBER DATA (CSV)                            │
│                                                                 │
│  olist_customers_dataset ──────────────────┐                    │
│  olist_products_dataset ───────────────┐   │                    │
│  olist_sellers_dataset ──────────────┐ │   │                    │
│  olist_orders_dataset ────────────┐  │ │   │                    │
│  olist_order_items_dataset ────┐  │  │ │   │                    │
│  product_category_name_translation ┘  │ │   │                   │
│                                      ▼ ▼ ▼ ▼                   │
│                              ╔══════════╗                      │
│                              ║   ETL    ║                      │
│                              ║  (PDI)   ║                      │
│                              ╚══════════╝                      │
│                                   │                            │
└───────────────────────────────────┼────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
     ┌──────────────┴──────┐  ┌────┴──────┐  ┌────┴──────────────┐
     │                  │  │          │  │                  │
     │   DIMENSI        │  │   FAKTA  │  │   DIMENSI        │
     │                  │  │          │  │                  │
     │ dim_customer ◄───┼──┤          ├──┼──► dim_product   │
     │                  │  │          │  │                  │
     │ dim_seller ◄─────┼──┤fact_sales│  │                  │
     │                  │  │          │  │                  │
     │ dim_date ◄───────┼──┤          │  │                  │
     │                  │  │          │  │                  │
     └──────────────────┘  └──────────┘  └──────────────────┘
```

### Struktur Final Data Warehouse

```sql
-- =============================================
-- TABEL DIMENSI
-- =============================================

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_seller;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_customer (
    customer_key INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(64),
    customer_unique_id VARCHAR(64),
    customer_city VARCHAR(100),
    customer_state VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_num INT,
    month_num INT,
    month_name VARCHAR(20),
    quarter_num INT,
    year_num INT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dim_product (
    product_key INT AUTO_INCREMENT PRIMARY KEY,
    product_id VARCHAR(64),
    product_category_name VARCHAR(255),
    product_category_name_english VARCHAR(255),
    product_weight_g DECIMAL(12,2),
    product_length_cm DECIMAL(12,2),
    product_height_cm DECIMAL(12,2),
    product_width_cm DECIMAL(12,2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE dim_seller (
    seller_key INT AUTO_INCREMENT PRIMARY KEY,
    seller_id VARCHAR(64),
    seller_city VARCHAR(100),
    seller_state VARCHAR(10)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- TABEL FAKTA
-- =============================================

CREATE TABLE fact_sales (
    sales_key BIGINT AUTO_INCREMENT PRIMARY KEY,
    customer_key INT,
    product_key INT,
    seller_key INT,
    date_key INT,
    price DECIMAL(12,2),
    freight_value DECIMAL(12,2),
    total_sales DECIMAL(12,2),

    INDEX idx_customer_key (customer_key),
    INDEX idx_product_key (product_key),
    INDEX idx_seller_key (seller_key),
    INDEX idx_date_key (date_key),

    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_key)
        REFERENCES dim_product(product_key),

    CONSTRAINT fk_fact_sales_seller
        FOREIGN KEY (seller_key)
        REFERENCES dim_seller(seller_key),

    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Mapping Source → DW

| Source (CSV) | Dim/Fact | Kolom Kunci |
|:-------------|:----------|:------------|
| `olist_customers_dataset` | `dim_customer` | `customer_id`, `customer_city`, `customer_state` |
| `olist_orders_dataset` | → `fact_sales` | `order_purchase_timestamp` → `dim_date` |
| `olist_products_dataset` | `dim_product` | `product_id`, `product_category_name` |
| `product_category_name_translation` | → `dim_product` | `product_category_name_english` |
| `olist_sellers_dataset` | `dim_seller` | `seller_id`, `seller_city`, `seller_state` |
| `olist_order_items_dataset` | `fact_sales` | `price`, `freight_value` |

---

## 🔗 Relasi dalam Star Schema

```
                    ┌──────────────────┐
                    │   dim_customer   │
                    │                  │◄──────────┐
                    │  customer_key (PK)│           │
                    │  customer_id      │           │
                    │  city, state      │           │
                    └──────────────────┘           │
                                                   │
                    ┌──────────────────┐           │
                    │   dim_product    │           │
                    │                  │◄──────────┼──┐
                    │  product_key (PK)│           │  │
                    │  product_id      │           │  │
                    │  category_name   │           │  │
                    │  weight, dims    │           │  │
                    └──────────────────┘           │  │
                                                   │  │
                    ┌──────────────────┐           │  │
                    │   dim_seller     │           │  │
                    │                  │◄──────────┼──┼──┐
                    │  seller_key (PK) │           │  │  │
                    │  seller_id       │           │  │  │
                    │  city, state     │           │  │  │
                    └──────────────────┘           │  │  │
                                                   │  │  │
                    ┌──────────────────┐           │  │  │
                    │    dim_date      │           │  │  │
                    │                  │◄──────────┼──┼──┼──┐
                    │  date_key (PK)   │           │  │  │  │
                    │  full_date       │           │  │  │  │
                    │  day, month, yr  │           │  │  │  │
                    └──────────────────┘           │  │  │  │
                                                   │  │  │  │
                    ┌─────────────────────────────────────────┐
                    │              fact_sales                  │
                    │  sales_key (PK)                         │
                    │  customer_key (FK) ─────────────────────┘  │  │  │
                    │  product_key (FK) ───────────────────────┘  │  │
                    │  seller_key (FK) ──────────────────────────┘  │
                    │  date_key (FK) ───────────────────────────────┘
                    │  price                                      │
                    │  freight_value                              │
                    │  total_sales                                │
                    └─────────────────────────────────────────────┘
```

---

## 🛠️ Teknologi yang Digunakan

| Tools | Kegunaan |
|-------|----------|
| **Python 3.10+** | Skrip otomatisasi identifikasi struktur & relasi dataset |
| **MySQL** | Database target untuk Data Warehouse |
| **Pentaho Data Integration (PDI)** | Proses ETL |
| **Pentaho `.ktr`** | Transformasi dimensi produk & transformasi utama |

---

## 🚀 Cara Menjalankan

```bash
# 1. Identifikasi struktur dataset
python main.py

# 2. Buat struktur Data Warehouse di MySQL
#    (jalankan script DDL di atas)

# 3. Jalankan ETL di Pentaho:
#    - Buka dim_produk.ktr
#    - Buka transformation1_uas.ktr
#    - Execute transformation
```

---

## 📊 Analisis yang Dapat Dilakukan

| Pertanyaan Bisnis | Fakta & Dimensi |
|------------------|-----------------|
| Berapa total penjualan per bulan? | `fact_sales.total_sales` + `dim_date.month_name` |
| Produk apa paling laris di tahun 2017? | `fact_sales` + `dim_product` + `dim_date` |
| Seller mana yang paling cepat kirim? | `fact_sales` + `dim_seller` (via freight_value & order_items) |
| Negara bagian mana penjualan tertinggi? | `fact_sales` + `dim_customer.state` |
| Kategori produk apa yang ratingnya terendah? | `fact_sales` + `dim_product.category` + review data |
| Bagaimana tren metode pembayaran per kuartal? | `fact_sales` + `dim_date.quarter_num` + payment data |

---

## 📚 Sumber Dataset

Dataset **Olist Brazilian E-Commerce** tersedia publik di [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

> Olist adalah platform e-commerce Brasil yang menghubungkan ribuan penjual kecil dengan jutaan pelanggan di seluruh Brasil — mirip seperti Tokopedia atau Shopee di Indonesia.

---

<p align="center">
  <sub>Tugas UAS Mata Kuliah Data Warehouse — 2026</sub>
  <br>
  <sub>Institut Teknologi dan Bisnis Ahmad Dahlan</sub>
</p>
