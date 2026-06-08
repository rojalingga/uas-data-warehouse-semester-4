# UAS Data Warehouse — Olist Brazilian E-Commerce

<p align="center">
  <img src="https://img.shields.io/badge/status-selesai-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/dataset-Olist%20Brazilian%20E--Commerce-blue" alt="Dataset">
  <img src="https://img.shields.io/badge/tools-Python%20%7C%20MySQL%20%7C%20Pentaho-orange" alt="Tools">
</p>

## 📌 Deskripsi Proyek

Proyek ini merupakan tugas akhir mata kuliah **Data Warehouse** yang membangun sistem **Data Warehouse (DW)** dari dataset publik **Olist Brazilian E-Commerce**. Dataset ini berisi data transaksi e-commerce Brasil dari tahun 2016 hingga 2018 yang mencakup **100 ribu pesanan**, **3 ribu seller**, dan **32 ribu produk** yang tersebar di berbagai negara bagian Brasil.

Proyek mencakup seluruh alur ETL (**Extract, Transform, Load**) mulai dari data mentah (CSV), transformasi menggunakan **Pentaho Data Integration (PDI) / Kettle**, hingga pemuatan ke dalam skema dimensional **Star Schema** di MySQL.

---

## 📂 Struktur Dataset

Dataset terdiri dari **9 file CSV** yang saling berelasi:

| File | Records | Deskripsi |
|------|---------|-----------|
| `olist_customers_dataset.csv` | 99.441 | Data pelanggan (ID unik, kode pos, kota, negara bagian) |
| `olist_geolocation_dataset.csv` | 1.000.164 | Data geolokasi (latitude, longitude, kode pos) |
| `olist_order_items_dataset.csv` | 112.650 | Item dalam setiap pesanan (produk, seller, harga, ongkir) |
| `olist_order_payments_dataset.csv` | 103.886 | Informasi pembayaran per pesanan |
| `olist_order_reviews_dataset.csv` | 104.720 | Ulasan pelanggan per pesanan (skor 1-5, komentar) |
| `olist_orders_dataset.csv` | 99.441 | Data utama pesanan (status, timestamp pengiriman) |
| `olist_products_dataset.csv` | 32.951 | Data produk (berat, dimensi, kategori, jumlah foto) |
| `olist_sellers_dataset.csv` | 3.095 | Data seller/penjual (kode pos, kota, negara bagian) |
| `product_category_name_translation.csv` | 71 | Terjemahan nama kategori produk (Portugis → Inggris) |

---

## 🗄️ Struktur MySQL & Relasi Antar Tabel

```sql
-- =============================================
-- TABEL DIMENSI
-- =============================================

-- Pelanggan (customer)
CREATE TABLE olist_customers_dataset (
    customer_id           VARCHAR(64)  NOT NULL,
    customer_unique_id    VARCHAR(64)  NOT NULL,
    customer_zip_code_prefix VARCHAR(64),
    customer_city         VARCHAR(255),
    customer_state        VARCHAR(255),
    PRIMARY KEY (customer_id)
);

-- Produk
CREATE TABLE olist_products_dataset (
    product_id               VARCHAR(64)  NOT NULL,
    product_category_name    VARCHAR(255),
    product_name_lenght      INT,
    product_description_lenght INT,
    product_photos_qty       INT,
    product_weight_g         DECIMAL(12,2),
    product_length_cm        DECIMAL(12,2),
    product_height_cm        DECIMAL(12,2),
    product_width_cm         INT,
    PRIMARY KEY (product_id)
);

-- Seller / Penjual
CREATE TABLE olist_sellers_dataset (
    seller_id              VARCHAR(64)  NOT NULL,
    seller_zip_code_prefix VARCHAR(64),
    seller_city            VARCHAR(255),
    seller_state           VARCHAR(255),
    PRIMARY KEY (seller_id)
);

-- Kategori Produk (terjemahan)
CREATE TABLE product_category_name_translation (
    product_category_name          VARCHAR(255),
    product_category_name_english  VARCHAR(255)
);

-- Geolokasi (referensi kode pos)
CREATE TABLE olist_geolocation_dataset (
    geolocation_zip_code_prefix VARCHAR(64),
    geolocation_lat             DECIMAL(12,2),
    geolocation_lng             DECIMAL(12,2),
    geolocation_city            VARCHAR(255),
    geolocation_state           VARCHAR(255)
);

-- =============================================
-- TABEL FAKTA
-- =============================================

-- Pesanan (Order Header)
CREATE TABLE olist_orders_dataset (
    order_id                       VARCHAR(64)  NOT NULL,
    customer_id                    VARCHAR(64)  NOT NULL,
    order_status                   VARCHAR(255),
    order_purchase_timestamp       DATETIME,
    order_approved_at              DATETIME,
    order_delivered_carrier_date   DATETIME,
    order_delivered_customer_date  DATETIME,
    order_estimated_delivery_date  DATETIME,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES olist_customers_dataset(customer_id)
);

-- Item Pesanan (Order Detail / Line Items)
CREATE TABLE olist_order_items_dataset (
    order_id            VARCHAR(64)  NOT NULL,
    order_item_id       VARCHAR(64)  NOT NULL,
    product_id          VARCHAR(64)  NOT NULL,
    seller_id           VARCHAR(64)  NOT NULL,
    shipping_limit_date DATETIME,
    price               DECIMAL(12,2),
    freight_value       DECIMAL(12,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id)   REFERENCES olist_orders_dataset(order_id),
    FOREIGN KEY (product_id) REFERENCES olist_products_dataset(product_id),
    FOREIGN KEY (seller_id)  REFERENCES olist_sellers_dataset(seller_id)
);

-- Pembayaran
CREATE TABLE olist_order_payments_dataset (
    order_id             VARCHAR(64)  NOT NULL,
    payment_sequential   INT,
    payment_type         VARCHAR(255),
    payment_installments INT,
    payment_value        DECIMAL(12,2),
    FOREIGN KEY (order_id) REFERENCES olist_orders_dataset(order_id)
);

-- Ulasan / Review
CREATE TABLE olist_order_reviews_dataset (
    review_id               VARCHAR(64)  NOT NULL,
    order_id                VARCHAR(64)  NOT NULL,
    review_score            INT,
    review_comment_title    VARCHAR(255),
    review_comment_message  VARCHAR(255),
    review_creation_date    DATETIME,
    review_answer_timestamp DATETIME,
    PRIMARY KEY (review_id),
    FOREIGN KEY (order_id) REFERENCES olist_orders_dataset(order_id)
);
```

---

## 🔗 Entity Relationship Diagram

```
    +------------------------------------------+
    |  olist_customers                          |
    |  customer_id (PK)  ----------------------+---+
    |  customer_unique_id                       |   |
    |  zip_code_prefix, city, state             |   |
    +------------------------------------------+   |
                                                   |
    +------------------------------------------+   |
    |  olist_orders                             |   |
    |  order_id (PK)                           |   |
    |  customer_id (FK) -----------------------+---+
    |  order_status, timestamp, dates          |
    +-----------------------+-------------------+
                            |
    +-----------------------+-------------------+   +----------------------------------+
    |  olist_order_items                         |   |  olist_products                    |
    |  order_id (FK) ----------------------------+   |  product_id (PK)                   |
    |  order_item_id                             |   |  product_category_name (FK) ------+---+
    |  product_id (FK) -------------------------+-->|  name, desc, weight, dimensions     |   |
    |  seller_id (FK) --------------------+     |   +------------------+----------------+   |
    |  price, freight_value              |     |                      |                      |
    +-------------------------------------+     |   +------------------+----------------+   |
                                                |   | product_category_name_translation |   |
    +-------------------------------------+     |   | product_category_name (PK) --------+---+
    |  olist_sellers                       |     |   | product_category_name_english      |
    |  seller_id (PK) ---------------------+-----+   +------------------------------------+
    |  zip_code_prefix, city, state       |
    +-------------------------------------+

    +------------------------------------------+
    |  olist_order_payments                    |
    |  order_id (FK) --------------------------+
    |  payment_sequential, payment_type        |
    |  payment_installments, payment_value     |
    +------------------------------------------+

    +------------------------------------------+
    |  olist_order_reviews                     |
    |  review_id (PK)                          |
    |  order_id (FK) --------------------------+
    |  review_score, review_comment, dates     |
    +------------------------------------------+
```

### Ringkasan Relasi

| # | Foreign Key | Referensi | Tipe |
|---|-------------|-----------|------|
| 1 | `olist_orders.customer_id` | → `olist_customers.customer_id` | Many-to-One |
| 2 | `olist_order_items.order_id` | → `olist_orders.order_id` | Many-to-One |
| 3 | `olist_order_items.product_id` | → `olist_products.product_id` | Many-to-One |
| 4 | `olist_order_items.seller_id` | → `olist_sellers.seller_id` | Many-to-One |
| 5 | `olist_order_payments.order_id` | → `olist_orders.order_id` | Many-to-One |
| 6 | `olist_order_reviews.order_id` | → `olist_orders.order_id` | Many-to-One |
| 7 | `olist_products.product_category_name` | → `product_category_name_translation.product_category_name` | Many-to-One |
| 8 | `olist_customers.zip_code_prefix` | → `olist_geolocation.zip_code_prefix` | Konseptual |
| 9 | `olist_sellers.zip_code_prefix` | → `olist_geolocation.zip_code_prefix` | Konseptual |

---

## 🛠️ Teknologi yang Digunakan

| Tools | Kegunaan |
|-------|----------|
| **Python 3.10+** | Skrip otomatisasi identifikasi struktur & relasi dataset |
| **MySQL** | Database target untuk Data Warehouse |
| **Pentaho Data Integration (PDI) / Kettle** | Proses ETL (Transformasi 1 & 2) |
| **Pentaho `dim_produk.ktr`** | Transformasi dimensi produk |
| **Pentaho `transformation1_uas.ktr`** | Transformasi utama ETL |

---

## 🚀 Cara Menjalankan

```bash
# 1. Identifikasi struktur dataset (otomatis)
python main.py

# 2. Import CSV ke MySQL (gunakan Pentaho atau LOAD DATA)
# 3. Jalankan transformasi ETL di Pentaho:
#    - dim_produk.ktr
#    - transformation1_uas.ktr
```

---

## 📊 Analisis yang Dapat Dilakukan

Dengan skema di atas, analisis berikut dapat dilakukan:

- **Analisis penjualan:** Total revenue per bulan, per kategori produk, per seller
- **Analisis pelanggan:** Customer segmentation berdasarkan frekuensi & nilai pesanan
- **Analisis pengiriman:** Performa on-time delivery, rata-rata waktu pengiriman per seller
- **Analisis pembayaran:** Distribusi metode pembayaran, cicilan rata-rata
- **Analisis kepuasan:** Skor review per produk/seller, korelasi review dengan waktu pengiriman
- **Analisis geografis:** Distribusi penjualan per negara bagian/kota

---

## 📚 Sumber Dataset

Dataset ini berasal dari **Olist Brazilian E-Commerce** yang tersedia secara publik di [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

> Olist adalah platform e-commerce Brasil yang menghubungkan penjual kecil dengan pelanggan melalui marketplace mereka.

---

<p align="center">
  <sub>Tugas UAS Mata Kuliah Data Warehouse — 2026</sub>
</p>
