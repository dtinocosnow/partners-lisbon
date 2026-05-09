#!/usr/bin/env python3
"""Generate audience-facing Snowflake Workspace Notebooks for Partners Lisbon demo."""

import json
import string
import random

def gen_id(length=8):
    """Generate unique 8-char alphanumeric cell ID."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

random.seed(42)

def md_cell(source):
    return {
        "cell_type": "markdown",
        "id": gen_id(),
        "metadata": {},
        "source": [source]
    }

def sql_cell(name, source):
    return {
        "cell_type": "code",
        "id": gen_id(),
        "metadata": {
            "codeCollapsed": False,
            "language": "sql",
            "name": name,
            "resultVariableName": name
        },
        "outputs": [],
        "execution_count": None,
        "source": [f"%%sql -r {name}\n{source}"]
    }

def py_cell(name, source):
    return {
        "cell_type": "code",
        "id": gen_id(),
        "metadata": {
            "codeCollapsed": False,
            "language": "python",
            "name": name
        },
        "outputs": [],
        "execution_count": None,
        "source": [source]
    }

def make_notebook(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.9.0"
            }
        },
        "cells": cells
    }


# =============================================================================
# NOTEBOOK 1: Aprofundamento I — Fundamentos da Plataforma
# =============================================================================

nb1_cells = []

# Title
nb1_cells.append(md_cell(
    "# ❄️ Aprofundamento I: Fundamentos da Plataforma Snowflake\n"
    "**Snowflake Partner Enablement — Lisboa 2026**\n\n"
    "---\n\n"
    "🎯 **Objetivo:** Demonstrar as capacidades core do Snowflake que resolvem problemas reais dos clientes.\n\n"
    "⏱️ **Duração:** ~35 minutos\n\n"
    "| # | Secção | Tempo | Conceito-chave |\n"
    "|---|--------|-------|----------------|\n"
    "| 1 | 🏗️ Setup do Ambiente | 3 min | Separação compute/storage |\n"
    "| 2 | 📦 Carga de Dados | 5 min | Formatos, tipos, escala |\n"
    "| 3 | 🔄 Snowpipe | 7 min | Ingestão contínua sem orquestração |\n"
    "| 4 | 🔒 Governança | 10 min | Mesma query, dados diferentes |\n"
    "| 5 | ⚡ Performance & Custos | 10 min | Pay-per-use, caching |\n\n"
    "---\n\n"
    "💡 **Como usar este notebook:** Execute cada célula sequencialmente. "
    "As explicações entre as células descrevem os conceitos-chave e o valor de negócio de cada funcionalidade."
))

# --- SECTION 1: Setup ---
nb1_cells.append(md_cell(
    "---\n"
    "## 1. 🏗️ Setup do Ambiente\n\n"
    "💡 **Conceito-chave:** A arquitetura do Snowflake separa completamente **compute** de **storage**. "
    "Isto significa que podemos escalar cada camada independentemente.\n\n"
    "🔑 **Porquê isto importa:** No Snowflake, toda a infraestrutura é criada instantaneamente via SQL — "
    "sem tickets de IT, sem aprovações, sem espera. Os clientes reduzem o time-to-value de semanas para segundos.\n\n"
    "```\n"
    "┌─────────────────────────────────────────────────────┐\n"
    "│  Cloud Services (Metadata, Otimização, Segurança)   │\n"
    "├─────────────────┬───────────────────────────────────┤\n"
    "│  Warehouse XS   │   Warehouse MEDIUM                │\n"
    "│  (Analistas)    │   (Engenheiros)                   │\n"
    "├─────────────────┴───────────────────────────────────┤\n"
    "│            Storage Centralizado (S3/Azure/GCS)      │\n"
    "└─────────────────────────────────────────────────────┘\n"
    "```"
))

nb1_cells.append(sql_cell("setup_db",
    "CREATE OR REPLACE DATABASE PARTNERS_LISBON_DEMO;\n\n"
    "CREATE OR REPLACE SCHEMA PARTNERS_LISBON_DEMO.RAW;\n"
    "CREATE OR REPLACE SCHEMA PARTNERS_LISBON_DEMO.ANALYTICS;\n"
    "CREATE OR REPLACE SCHEMA PARTNERS_LISBON_DEMO.GOVERNANCE;"
))

nb1_cells.append(sql_cell("setup_wh",
    "CREATE OR REPLACE WAREHOUSE PARTNERS_WH\n"
    "    WAREHOUSE_SIZE = 'XSMALL'\n"
    "    AUTO_SUSPEND = 60\n"
    "    AUTO_RESUME = TRUE\n"
    "    INITIALLY_SUSPENDED = TRUE;\n\n"
    "CREATE OR REPLACE WAREHOUSE PARTNERS_WH_MEDIUM\n"
    "    WAREHOUSE_SIZE = 'MEDIUM'\n"
    "    AUTO_SUSPEND = 60\n"
    "    AUTO_RESUME = TRUE\n"
    "    INITIALLY_SUSPENDED = TRUE;"
))

nb1_cells.append(sql_cell("setup_roles",
    "CREATE OR REPLACE ROLE ANALYST_ROLE;\n"
    "CREATE OR REPLACE ROLE ENGINEER_ROLE;\n\n"
    "GRANT USAGE ON DATABASE PARTNERS_LISBON_DEMO TO ROLE ANALYST_ROLE;\n"
    "GRANT USAGE ON DATABASE PARTNERS_LISBON_DEMO TO ROLE ENGINEER_ROLE;\n"
    "GRANT USAGE ON SCHEMA PARTNERS_LISBON_DEMO.RAW TO ROLE ANALYST_ROLE;\n"
    "GRANT USAGE ON SCHEMA PARTNERS_LISBON_DEMO.RAW TO ROLE ENGINEER_ROLE;\n"
    "GRANT USAGE ON SCHEMA PARTNERS_LISBON_DEMO.ANALYTICS TO ROLE ANALYST_ROLE;\n"
    "GRANT USAGE ON SCHEMA PARTNERS_LISBON_DEMO.ANALYTICS TO ROLE ENGINEER_ROLE;\n"
    "GRANT SELECT ON ALL TABLES IN SCHEMA PARTNERS_LISBON_DEMO.RAW TO ROLE ANALYST_ROLE;\n"
    "GRANT ALL ON SCHEMA PARTNERS_LISBON_DEMO.RAW TO ROLE ENGINEER_ROLE;\n"
    "GRANT USAGE ON WAREHOUSE PARTNERS_WH TO ROLE ANALYST_ROLE;\n"
    "GRANT USAGE ON WAREHOUSE PARTNERS_WH TO ROLE ENGINEER_ROLE;\n"
    "GRANT USAGE ON WAREHOUSE PARTNERS_WH_MEDIUM TO ROLE ENGINEER_ROLE;"
))

nb1_cells.append(md_cell(
    "✅ **Resultado:** Em segundos criámos toda a infraestrutura — "
    "base de dados, schemas, warehouses e roles com permissões granulares.\n\n"
    "⚡ Os warehouses estão `INITIALLY_SUSPENDED` — zero custo até serem usados. "
    "`AUTO_RESUME=TRUE` liga-os automaticamente na primeira query."
))

# --- SECTION 2: Data Loading ---
nb1_cells.append(md_cell(
    "---\n"
    "## 2. 📦 Carga de Dados\n\n"
    "💡 **Conceito-chave:** O Snowflake aceita CSV, JSON, Parquet, Avro, ORC e XML — "
    "tudo sem ETL externo. É schema-on-read E schema-on-write.\n\n"
    "🔑 **Porquê isto importa:** Os clientes não precisam de transformar dados "
    "antes de os carregar — eliminando ferramentas intermediárias e acelerando o onboarding de novas fontes.\n\n"
    "| Formato | Semi-estruturado? | Caso de Uso Típico |\n"
    "|---------|-------------------|-----------|\n"
    "| CSV | ❌ | Exports de sistemas legados |\n"
    "| JSON | ✅ | APIs, eventos, logs |\n"
    "| Parquet | ✅ | Data lakes, analytics |\n"
    "| Avro | ✅ | Streaming (Kafka) |\n"
    "| ORC | ✅ | Migração de Hadoop |"
))

nb1_cells.append(sql_cell("use_schema",
    "USE WAREHOUSE PARTNERS_WH;\nUSE SCHEMA PARTNERS_LISBON_DEMO.RAW;"
))

nb1_cells.append(sql_cell("create_customers",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.customers (\n"
    "    customer_id INT,\n"
    "    first_name VARCHAR(50),\n"
    "    last_name VARCHAR(50),\n"
    "    email VARCHAR(100),\n"
    "    phone VARCHAR(30),\n"
    "    city VARCHAR(50),\n"
    "    country VARCHAR(50),\n"
    "    region VARCHAR(10),\n"
    "    signup_date DATE,\n"
    "    customer_tier VARCHAR(10)\n"
    ");\n\n"
    "INSERT INTO PARTNERS_LISBON_DEMO.RAW.customers VALUES\n"
    "(1,'Joao','Silva','joao.silva@email.pt','+351 912 345 678','Lisboa','Portugal','EMEA','2024-01-15','Gold'),\n"
    "(2,'Maria','Santos','maria.santos@email.pt','+351 923 456 789','Porto','Portugal','EMEA','2024-02-20','Silver'),\n"
    "(3,'Pedro','Costa','pedro.costa@email.pt','+351 934 567 890','Faro','Portugal','EMEA','2024-03-10','Bronze'),\n"
    "(4,'Ana','Ferreira','ana.ferreira@email.pt','+351 945 678 901','Coimbra','Portugal','EMEA','2024-04-05','Gold'),\n"
    "(5,'Miguel','Oliveira','miguel.oliveira@email.es','+34 612 345 678','Madrid','Spain','EMEA','2024-01-25','Silver'),\n"
    "(6,'Sofia','Rodriguez','sofia.rodriguez@email.es','+34 623 456 789','Barcelona','Spain','EMEA','2024-05-12','Gold'),\n"
    "(7,'Hans','Mueller','hans.mueller@email.de','+49 151 234 5678','Berlin','Germany','EMEA','2024-02-28','Bronze'),\n"
    "(8,'Pierre','Dupont','pierre.dupont@email.fr','+33 612 345 678','Paris','France','EMEA','2024-06-01','Silver'),\n"
    "(9,'John','Smith','john.smith@email.com','+1 212 345 6789','New York','United States','AMER','2024-03-15','Gold'),\n"
    "(10,'Sarah','Johnson','sarah.johnson@email.com','+1 310 456 7890','Los Angeles','United States','AMER','2024-04-20','Silver'),\n"
    "(11,'Carlos','Mendes','carlos.mendes@email.pt','+351 956 789 012','Braga','Portugal','EMEA','2024-07-01','Bronze'),\n"
    "(12,'Isabella','Rossi','isabella.rossi@email.it','+39 331 234 5678','Milan','Italy','EMEA','2024-05-18','Gold'),\n"
    "(13,'Yuki','Tanaka','yuki.tanaka@email.jp','+81 90 1234 5678','Tokyo','Japan','APJ','2024-06-15','Silver'),\n"
    "(14,'Wei','Chen','wei.chen@email.cn','+86 138 1234 5678','Shanghai','China','APJ','2024-07-10','Gold'),\n"
    "(15,'Emma','Wilson','emma.wilson@email.co.uk','+44 7911 123456','London','United Kingdom','EMEA','2024-08-01','Bronze');"
))

nb1_cells.append(sql_cell("create_products",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.products (\n"
    "    product_id INT,\n"
    "    product_name VARCHAR(100),\n"
    "    category VARCHAR(50),\n"
    "    subcategory VARCHAR(50),\n"
    "    unit_price DECIMAL(10,2),\n"
    "    cost_price DECIMAL(10,2),\n"
    "    description VARCHAR(200)\n"
    ");\n\n"
    "INSERT INTO PARTNERS_LISBON_DEMO.RAW.products VALUES\n"
    "(101,'Laptop Pro 15','Electronics','Laptops',1299.99,850.00,'High-performance laptop with 15-inch display'),\n"
    "(102,'Laptop Air 13','Electronics','Laptops',999.99,650.00,'Ultra-thin laptop for professionals'),\n"
    "(103,'Wireless Mouse Elite','Accessories','Mice',79.99,35.00,'Ergonomic wireless mouse'),\n"
    "(104,'Mechanical Keyboard Pro','Accessories','Keyboards',149.99,65.00,'RGB mechanical keyboard'),\n"
    "(105,'Monitor UltraWide 34','Electronics','Monitors',699.99,420.00,'Ultra-wide curved monitor'),\n"
    "(106,'USB-C Hub 7-in-1','Accessories','Hubs',59.99,22.00,'Multi-port USB-C hub'),\n"
    "(107,'Noise-Cancelling Headphones','Audio','Headphones',349.99,180.00,'Premium wireless headphones'),\n"
    "(108,'Webcam HD 4K','Electronics','Cameras',129.99,55.00,'4K webcam with auto-focus'),\n"
    "(109,'External SSD 1TB','Storage','Drives',119.99,60.00,'Portable SSD USB 3.2'),\n"
    "(110,'Tablet Pro 11','Electronics','Tablets',899.99,580.00,'11-inch tablet with stylus'),\n"
    "(111,'Wireless Charger Pad','Accessories','Chargers',39.99,12.00,'Fast wireless charger'),\n"
    "(112,'Bluetooth Speaker','Audio','Speakers',89.99,38.00,'Portable waterproof speaker');"
))

nb1_cells.append(sql_cell("create_orders",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.orders (\n"
    "    order_id INT,\n"
    "    customer_id INT,\n"
    "    order_date DATE,\n"
    "    order_status VARCHAR(20),\n"
    "    shipping_method VARCHAR(20),\n"
    "    total_amount DECIMAL(10,2)\n"
    ");\n\n"
    "INSERT INTO PARTNERS_LISBON_DEMO.RAW.orders VALUES\n"
    "(1001,1,'2025-01-05','Delivered','Express',1379.98),\n"
    "(1002,2,'2025-01-12','Delivered','Standard',999.99),\n"
    "(1003,3,'2025-01-20','Delivered','Express',229.98),\n"
    "(1004,4,'2025-02-01','Delivered','Standard',1299.99),\n"
    "(1005,5,'2025-02-10','Delivered','Express',449.98),\n"
    "(1006,6,'2025-02-18','Delivered','Standard',699.99),\n"
    "(1007,7,'2025-02-25','Delivered','Express',149.99),\n"
    "(1008,8,'2025-03-05','Delivered','Standard',1899.98),\n"
    "(1009,9,'2025-03-12','Delivered','Express',349.99),\n"
    "(1010,10,'2025-03-20','Delivered','Standard',239.98),\n"
    "(1011,1,'2025-03-28','Delivered','Express',899.99),\n"
    "(1012,11,'2025-04-05','Delivered','Standard',79.99),\n"
    "(1013,12,'2025-04-12','Delivered','Express',1349.98),\n"
    "(1014,13,'2025-04-20','Shipped','Standard',469.98),\n"
    "(1015,14,'2025-04-28','Shipped','Express',2199.98),\n"
    "(1016,2,'2025-05-05','Shipped','Standard',129.99),\n"
    "(1017,4,'2025-05-12','Shipped','Express',349.99),\n"
    "(1018,6,'2025-05-20','Processing','Standard',1599.98),\n"
    "(1019,9,'2025-05-28','Processing','Express',179.98),\n"
    "(1020,15,'2025-06-05','Processing','Standard',899.99),\n"
    "(1021,1,'2025-06-10','Processing','Express',259.98),\n"
    "(1022,3,'2025-06-15','Pending','Standard',1299.99),\n"
    "(1023,5,'2025-06-20','Pending','Express',89.99),\n"
    "(1024,7,'2025-06-25','Pending','Standard',449.98),\n"
    "(1025,8,'2025-06-30','Pending','Express',119.99),\n"
    "(1026,10,'2025-07-01','Pending','Standard',699.99),\n"
    "(1027,12,'2025-07-02','Pending','Express',39.99),\n"
    "(1028,14,'2025-07-03','Pending','Standard',1299.99),\n"
    "(1029,11,'2025-07-04','Pending','Express',209.98),\n"
    "(1030,15,'2025-07-05','Pending','Standard',349.99);"
))

nb1_cells.append(sql_cell("create_order_items",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.order_items (\n"
    "    item_id INT,\n"
    "    order_id INT,\n"
    "    product_id INT,\n"
    "    quantity INT,\n"
    "    unit_price DECIMAL(10,2),\n"
    "    discount_pct DECIMAL(5,2)\n"
    ");\n\n"
    "INSERT INTO PARTNERS_LISBON_DEMO.RAW.order_items VALUES\n"
    "(1,1001,101,1,1299.99,0),\n"
    "(2,1001,103,1,79.99,0),\n"
    "(3,1002,102,1,999.99,0),\n"
    "(4,1003,104,1,149.99,0),\n"
    "(5,1003,103,1,79.99,0),\n"
    "(6,1004,101,1,1299.99,0),\n"
    "(7,1005,107,1,349.99,0),\n"
    "(8,1005,106,1,59.99,10),\n"
    "(9,1006,105,1,699.99,0),\n"
    "(10,1007,104,1,149.99,0),\n"
    "(11,1008,101,1,1299.99,5),\n"
    "(12,1008,105,1,699.99,0),\n"
    "(13,1009,107,1,349.99,0),\n"
    "(14,1010,103,2,79.99,0),\n"
    "(15,1010,111,2,39.99,5),\n"
    "(16,1011,110,1,899.99,0),\n"
    "(17,1012,103,1,79.99,0),\n"
    "(18,1013,101,1,1299.99,0),\n"
    "(19,1013,111,1,39.99,10),\n"
    "(20,1014,107,1,349.99,0),\n"
    "(21,1014,109,1,119.99,0),\n"
    "(22,1015,101,1,1299.99,0),\n"
    "(23,1015,110,1,899.99,0),\n"
    "(24,1016,108,1,129.99,0),\n"
    "(25,1017,107,1,349.99,0),\n"
    "(26,1018,102,1,999.99,5),\n"
    "(27,1018,105,1,699.99,0),\n"
    "(28,1019,106,2,59.99,0),\n"
    "(29,1019,111,1,39.99,10),\n"
    "(30,1020,110,1,899.99,0),\n"
    "(31,1021,104,1,149.99,0),\n"
    "(32,1021,109,1,119.99,0),\n"
    "(33,1022,101,1,1299.99,0),\n"
    "(34,1023,112,1,89.99,0),\n"
    "(35,1024,107,1,349.99,5),\n"
    "(36,1024,106,1,59.99,10),\n"
    "(37,1025,109,1,119.99,0),\n"
    "(38,1026,105,1,699.99,0),\n"
    "(39,1027,111,1,39.99,0),\n"
    "(40,1028,101,1,1299.99,0),\n"
    "(41,1029,103,1,79.99,0),\n"
    "(42,1029,108,1,129.99,0),\n"
    "(43,1030,107,1,349.99,0),\n"
    "(44,1005,112,1,89.99,0),\n"
    "(45,1008,106,1,59.99,0),\n"
    "(46,1013,106,1,59.99,0),\n"
    "(47,1015,104,1,149.99,5),\n"
    "(48,1018,108,1,129.99,0),\n"
    "(49,1024,112,1,89.99,0),\n"
    "(50,1030,111,1,39.99,0);"
))

nb1_cells.append(sql_cell("create_reviews",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.product_reviews (\n"
    "    review_id INT,\n"
    "    product_id INT,\n"
    "    customer_id INT,\n"
    "    review_date DATE,\n"
    "    rating INT,\n"
    "    review_text VARCHAR(500)\n"
    ");\n\n"
    "INSERT INTO PARTNERS_LISBON_DEMO.RAW.product_reviews VALUES\n"
    "(1,101,1,'2025-01-20',5,'Excellent laptop, very fast and the display is amazing. Best purchase I made this year.'),\n"
    "(2,102,2,'2025-01-25',4,'Great thin laptop, perfect for travel. Battery life could be slightly better.'),\n"
    "(3,103,3,'2025-02-05',3,'Decent mouse but nothing special. Works fine for daily use.'),\n"
    "(4,104,4,'2025-02-15',5,'Love the mechanical feel and RGB lighting. Very satisfying to type on.'),\n"
    "(5,105,6,'2025-03-01',5,'The ultra-wide monitor is incredible for productivity. Highly recommend.'),\n"
    "(6,107,9,'2025-03-15',4,'Great noise cancellation. Sound quality is premium. Comfortable for long sessions.'),\n"
    "(7,101,12,'2025-04-15',5,'Powerful machine, handles everything I throw at it. Worth every penny.'),\n"
    "(8,110,1,'2025-04-01',4,'Nice tablet, stylus works great. Wish it had more storage options.'),\n"
    "(9,106,8,'2025-03-10',2,'Hub stopped working after a month. Disappointing quality for the price.'),\n"
    "(10,109,10,'2025-03-25',4,'Fast and reliable SSD. Transfer speeds are impressive.'),\n"
    "(11,108,14,'2025-05-01',3,'Webcam is okay, 4K quality is good but software is buggy.'),\n"
    "(12,111,5,'2025-02-15',1,'Charger overheated and stopped working in two weeks. Terrible product.'),\n"
    "(13,112,7,'2025-03-05',4,'Good sound for the size. Waterproof design is great for outdoor use.'),\n"
    "(14,107,4,'2025-05-15',5,'Second pair I bought - giving one as a gift. Absolutely love them.'),\n"
    "(15,102,15,'2025-06-10',4,'Solid laptop for the price. Fast boot times and nice keyboard.');"
))

nb1_cells.append(sql_cell("verify_load",
    "SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM PARTNERS_LISBON_DEMO.RAW.customers\n"
    "UNION ALL\n"
    "SELECT 'products', COUNT(*) FROM PARTNERS_LISBON_DEMO.RAW.products\n"
    "UNION ALL\n"
    "SELECT 'orders', COUNT(*) FROM PARTNERS_LISBON_DEMO.RAW.orders\n"
    "UNION ALL\n"
    "SELECT 'order_items', COUNT(*) FROM PARTNERS_LISBON_DEMO.RAW.order_items\n"
    "UNION ALL\n"
    "SELECT 'product_reviews', COUNT(*) FROM PARTNERS_LISBON_DEMO.RAW.product_reviews;"
))

nb1_cells.append(py_cell("viz_row_counts",
    "import matplotlib.pyplot as plt\n\n"
    "tables = verify_load['TABLE_NAME'].tolist()\n"
    "counts = verify_load['ROW_COUNT'].tolist()\n\n"
    "fig, ax = plt.subplots(figsize=(8, 4))\n"
    "bars = ax.bar(tables, counts, color=['#29B5E8', '#11567F', '#7D44CF', '#FF9F36', '#71D3DC'])\n"
    "ax.set_title('📦 Contagem de Registos por Tabela', fontsize=14, fontweight='bold')\n"
    "ax.set_xlabel('Tabela')\n"
    "ax.set_ylabel('Número de Registos')\n"
    "for bar, count in zip(bars, counts):\n"
    "    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,\n"
    "            str(count), ha='center', va='bottom', fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

nb1_cells.append(md_cell(
    "✅ **Resultado:** 5 tabelas criadas e carregadas com dados realistas — "
    "clientes de 9 países, 12 produtos, 30 encomendas.\n\n"
    "💡 **Nota importante:** Usámos INSERT para a demo, mas em produção usaríamos:\n"
    "- `COPY INTO` para cargas batch de ficheiros\n"
    "- `Snowpipe` para ingestão contínua (que vemos a seguir!)\n"
    "- `Snowpipe Streaming` para real-time via SDK"
))

# --- SECTION 3: Snowpipe ---
nb1_cells.append(md_cell(
    "---\n"
    "## 3. 🔄 Snowpipe — Ingestão Contínua\n\n"
    "💡 **Conceito-chave:** O Snowpipe monitoriza ficheiros novos num stage e carrega-os "
    "automaticamente — zero intervenção humana, zero orquestração.\n\n"
    "🔑 **Porquê isto importa:** Elimina a complexidade de manter pipelines de ingestão "
    "(cron jobs, Airflow, scripts custom). Os dados ficam disponíveis em ~1 minuto após chegarem ao stage.\n\n"
    "| Método | Latência | Orquestração | Caso de Uso |\n"
    "|--------|----------|--------------|-------------|\n"
    "| COPY INTO | Minutos | Manual/Schedule | Batch tradicional |\n"
    "| Snowpipe | ~1 min | Automática (notificações S3/Azure/GCS) | Streaming de ficheiros |\n"
    "| Snowpipe Streaming | <10s | SDK (Java/Python) | Real-time de baixa latência |\n\n"
    "⚡ **Nota:** Snowpipe usa compute serverless — paga-se apenas pelo tempo de ingestão, "
    "sem warehouse dedicado."
))

nb1_cells.append(sql_cell("snowpipe_stage",
    "CREATE OR REPLACE STAGE PARTNERS_LISBON_DEMO.RAW.partners_ingest_stage\n"
    "    FILE_FORMAT = (TYPE = 'JSON');"
))

nb1_cells.append(sql_cell("snowpipe_table",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.raw_events (\n"
    "    event_id INT,\n"
    "    event_type VARCHAR(50),\n"
    "    event_timestamp TIMESTAMP_NTZ,\n"
    "    user_id INT,\n"
    "    event_data VARIANT,\n"
    "    loaded_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()\n"
    ");"
))

nb1_cells.append(sql_cell("snowpipe_create",
    "CREATE OR REPLACE PIPE PARTNERS_LISBON_DEMO.RAW.partners_event_pipe\n"
    "    AUTO_INGEST = FALSE\n"
    "AS\n"
    "COPY INTO PARTNERS_LISBON_DEMO.RAW.raw_events (event_id, event_type, event_timestamp, user_id, event_data)\n"
    "FROM (\n"
    "    SELECT\n"
    "        $1:event_id::INT,\n"
    "        $1:event_type::VARCHAR,\n"
    "        $1:event_timestamp::TIMESTAMP_NTZ,\n"
    "        $1:user_id::INT,\n"
    "        $1:event_data::VARIANT\n"
    "    FROM @PARTNERS_LISBON_DEMO.RAW.partners_ingest_stage\n"
    ");"
))

nb1_cells.append(md_cell(
    "👇 A seguir geramos 20 eventos JSON sintéticos e colocamo-los no stage. "
    "Em produção, estes ficheiros chegariam via notificação S3 ou Azure Event Grid, "
    "e o Snowpipe carregá-los-ia automaticamente."
))

nb1_cells.append(sql_cell("snowpipe_generate",
    "COPY INTO @PARTNERS_LISBON_DEMO.RAW.partners_ingest_stage/events/batch_001.json\n"
    "FROM (\n"
    "    SELECT OBJECT_CONSTRUCT(\n"
    "        'event_id', SEQ4(),\n"
    "        'event_type', CASE MOD(SEQ4(), 4)\n"
    "            WHEN 0 THEN 'page_view'\n"
    "            WHEN 1 THEN 'add_to_cart'\n"
    "            WHEN 2 THEN 'purchase'\n"
    "            WHEN 3 THEN 'search'\n"
    "        END,\n"
    "        'event_timestamp', DATEADD('minute', -SEQ4() * 15, CURRENT_TIMESTAMP()),\n"
    "        'user_id', MOD(SEQ4(), 15) + 1,\n"
    "        'event_data', OBJECT_CONSTRUCT(\n"
    "            'page', '/products/' || (MOD(SEQ4(), 12) + 101),\n"
    "            'session_id', UUID_STRING(),\n"
    "            'device', CASE MOD(SEQ4(), 3) WHEN 0 THEN 'mobile' WHEN 1 THEN 'desktop' ELSE 'tablet' END\n"
    "        )\n"
    "    ) AS json_data\n"
    "    FROM TABLE(GENERATOR(ROWCOUNT => 20))\n"
    ");"
))

nb1_cells.append(sql_cell("snowpipe_refresh",
    "ALTER PIPE PARTNERS_LISBON_DEMO.RAW.partners_event_pipe REFRESH;"
))

nb1_cells.append(sql_cell("snowpipe_status",
    "SELECT SYSTEM$PIPE_STATUS('PARTNERS_LISBON_DEMO.RAW.partners_event_pipe');"
))

nb1_cells.append(sql_cell("snowpipe_count",
    "SELECT COUNT(*) AS event_count FROM PARTNERS_LISBON_DEMO.RAW.raw_events;"
))

nb1_cells.append(md_cell(
    "✅ **Resultado:** Pipeline de ingestão completo em funcionamento:\n"
    "1. Stage para receber ficheiros\n"
    "2. Pipe com transformação (JSON → tabela relacional)\n"
    "3. Dados carregados automaticamente\n\n"
    "🔑 **Em produção:** Configuramos uma notificação S3/Azure/GCS → o Snowpipe carrega "
    "automaticamente cada ficheiro novo em ~1 minuto. **Zero orquestração, zero manutenção.**"
))

# --- SECTION 4: Governance ---
nb1_cells.append(md_cell(
    "---\n"
    "## 4. 🔒 Governança de Dados — O Momento WOW!\n\n"
    "💡 **Conceito-chave:** A governança está nos **DADOS**, não na aplicação. "
    "Masking policies e row access policies são aplicadas automaticamente — "
    "a aplicação nem sabe que existem.\n\n"
    "🔑 **Porquê isto importa:** Com uma única policy SQL, garantimos que dados sensíveis "
    "ficam protegidos para TODAS as ferramentas de acesso (BI, SQL, APIs, Python) — "
    "sem alterações de código. Conformidade GDPR/LGPD automática.\n\n"
    "🔥 Vamos ver como a **MESMA query**, executada pelo **MESMO utilizador**, "
    "retorna dados **DIFERENTES** baseado no role ativo."
))

nb1_cells.append(sql_cell("mask_email",
    "CREATE OR REPLACE MASKING POLICY PARTNERS_LISBON_DEMO.GOVERNANCE.mask_email AS\n"
    "(val STRING) RETURNS STRING ->\n"
    "    CASE\n"
    "        WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'ENGINEER_ROLE') THEN val\n"
    "        ELSE REGEXP_REPLACE(val, '.+@', '****@')\n"
    "    END;\n\n"
    "ALTER TABLE PARTNERS_LISBON_DEMO.RAW.customers\n"
    "    MODIFY COLUMN email SET MASKING POLICY PARTNERS_LISBON_DEMO.GOVERNANCE.mask_email;"
))

nb1_cells.append(sql_cell("mask_phone",
    "CREATE OR REPLACE MASKING POLICY PARTNERS_LISBON_DEMO.GOVERNANCE.mask_phone AS\n"
    "(val STRING) RETURNS STRING ->\n"
    "    CASE\n"
    "        WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'ENGINEER_ROLE') THEN val\n"
    "        ELSE CONCAT(LEFT(val, 4), ' *** *** ***')\n"
    "    END;\n\n"
    "ALTER TABLE PARTNERS_LISBON_DEMO.RAW.customers\n"
    "    MODIFY COLUMN phone SET MASKING POLICY PARTNERS_LISBON_DEMO.GOVERNANCE.mask_phone;"
))

nb1_cells.append(sql_cell("row_access",
    "CREATE OR REPLACE ROW ACCESS POLICY PARTNERS_LISBON_DEMO.GOVERNANCE.region_access_policy AS\n"
    "(region_val VARCHAR) RETURNS BOOLEAN ->\n"
    "    CASE\n"
    "        WHEN CURRENT_ROLE() = 'ACCOUNTADMIN' THEN TRUE\n"
    "        WHEN CURRENT_ROLE() = 'ANALYST_ROLE' AND region_val = 'EMEA' THEN TRUE\n"
    "        ELSE FALSE\n"
    "    END;\n\n"
    "ALTER TABLE PARTNERS_LISBON_DEMO.RAW.customers\n"
    "    ADD ROW ACCESS POLICY PARTNERS_LISBON_DEMO.GOVERNANCE.region_access_policy ON (region);"
))

nb1_cells.append(md_cell(
    "### 👁️ Visibilidade como ACCOUNTADMIN (acesso total)\n\n"
    "👁️ Como ACCOUNTADMIN, temos visibilidade total sobre todos os dados — emails completos, "
    "telefones completos, todas as regiões. No próximo passo veremos como isto muda com roles diferentes."
))

nb1_cells.append(sql_cell("gov_full_view",
    "SELECT customer_id, first_name, last_name, email, phone, city, country, region\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.customers\n"
    "LIMIT 5;"
))

nb1_cells.append(md_cell(
    "### 📊 Contagem por região\n\n"
    "👁️ Como ACCOUNTADMIN vemos as 3 regiões (EMEA: 11, AMER: 2, APJ: 2). "
    "Se executássemos como ANALYST_ROLE, veríamos **APENAS EMEA** — a row access policy filtra automaticamente."
))

nb1_cells.append(sql_cell("gov_region_counts",
    "SELECT region, COUNT(*) AS customer_count\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.customers\n"
    "GROUP BY region\n"
    "ORDER BY customer_count DESC;"
))

nb1_cells.append(md_cell(
    "### 🎯 Comparação de Visibilidade por Role\n\n"
    "| | 👑 ACCOUNTADMIN | 📊 ANALYST_ROLE |\n"
    "|---|---|---|\n"
    "| **Email** | joao.silva@email.pt | ****@email.pt |\n"
    "| **Telefone** | +351 912 345 678 | +351 *** *** *** |\n"
    "| **Regiões visíveis** | EMEA, AMER, APJ (15 registos) | Apenas EMEA (11 registos) |\n"
    "| **Dados** | Tudo visível | Apenas a sua região |\n\n"
    "✅ **Resultado:** A mesma tabela, a mesma query, mas resultados completamente "
    "diferentes baseados no role. **Zero código na aplicação.**\n\n"
    "💡 **Conceito-chave:** A governança está nos DADOS, não na app. "
    "Qualquer ferramenta (Tableau, Power BI, Python, dbt) respeita estas policies automaticamente."
))

# --- SECTION 5: Performance & Cost ---
nb1_cells.append(md_cell(
    "---\n"
    "## 5. ⚡ Performance & Gestão de Custos\n\n"
    "💡 **Conceito-chave:** O modelo pay-per-second com auto-suspend garante que "
    "só pagamos quando estamos a usar compute. Controlo total sobre custos.\n\n"
    "🔑 **Porquê isto importa:** Os clientes preocupam-se com custos imprevisíveis "
    "na cloud. O Snowflake dá-lhes visibilidade e controlo granular.\n\n"
    "| Tamanho | Créditos/h | Nós | Caso de Uso |\n"
    "|---------|------------|-----|-------------|\n"
    "| XS | 1 | 1 | Dev, queries simples |\n"
    "| S | 2 | 2 | BI, relatórios |\n"
    "| M | 4 | 4 | ETL, analytics |\n"
    "| L | 8 | 8 | Cargas pesadas |\n"
    "| XL+ | 16-512 | 16-512 | Big data, ML |\n\n"
    "⚡ **3 níveis de cache** (do mais rápido ao mais lento):\n"
    "1. 🟢 **Result Cache** — Resultado idêntico em <100ms (24h)\n"
    "2. 🟡 **Local Disk Cache** — SSD do warehouse (dados quentes)\n"
    "3. 🔵 **Remote Disk Cache** — Storage centralizado"
))

nb1_cells.append(sql_cell("revenue_query",
    "SELECT\n"
    "    p.category,\n"
    "    p.subcategory,\n"
    "    COUNT(DISTINCT o.order_id) AS num_orders,\n"
    "    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS total_revenue,\n"
    "    AVG(oi.unit_price) AS avg_unit_price\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.orders o\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.order_items oi ON o.order_id = oi.order_id\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.products p ON oi.product_id = p.product_id\n"
    "GROUP BY p.category, p.subcategory\n"
    "ORDER BY total_revenue DESC;"
))

nb1_cells.append(py_cell("viz_revenue",
    "import matplotlib.pyplot as plt\n\n"
    "df = revenue_query.sort_values('TOTAL_REVENUE', ascending=True)\n\n"
    "fig, ax = plt.subplots(figsize=(10, 6))\n"
    "colors = ['#29B5E8' if cat == 'Electronics' else '#7D44CF' if cat == 'Audio' else '#FF9F36' if cat == 'Accessories' else '#71D3DC'\n"
    "          for cat in df['CATEGORY']]\n"
    "bars = ax.barh(df['SUBCATEGORY'], df['TOTAL_REVENUE'], color=colors)\n"
    "ax.set_title('⚡ Receita por Subcategoria', fontsize=14, fontweight='bold')\n"
    "ax.set_xlabel('Receita Total (€)')\n"
    "ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

nb1_cells.append(md_cell(
    "### 🚀 Demonstração de Cache\n\n"
    "💡 **Conceito-chave:** O Result Cache guarda resultados de queries idênticas durante 24h. "
    "Execute a query abaixo **DUAS VEZES** — a segunda execução será **instantânea** (~0ms) "
    "porque reutiliza o resultado em cache.\n\n"
    "▶️ **Exercício:** Executar → ver tempo → executar novamente → ver tempo"
))

nb1_cells.append(sql_cell("cache_demo",
    "SELECT\n"
    "    p.category,\n"
    "    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS total_revenue\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.orders o\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.order_items oi ON o.order_id = oi.order_id\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.products p ON oi.product_id = p.product_id\n"
    "GROUP BY p.category\n"
    "ORDER BY total_revenue DESC;"
))

nb1_cells.append(md_cell(
    "### 📊 Tamanhos de Warehouse & Créditos"
))

nb1_cells.append(py_cell("viz_wh_sizes",
    "import matplotlib.pyplot as plt\n\n"
    "sizes = ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL']\n"
    "credits = [1, 2, 4, 8, 16, 32, 64, 128]\n\n"
    "fig, ax = plt.subplots(figsize=(9, 5))\n"
    "bars = ax.bar(sizes, credits, color='#29B5E8', edgecolor='#11567F', linewidth=1.2)\n"
    "ax.set_title('💰 Créditos por Hora vs Tamanho do Warehouse', fontsize=14, fontweight='bold')\n"
    "ax.set_xlabel('Tamanho do Warehouse')\n"
    "ax.set_ylabel('Créditos / Hora')\n"
    "ax.set_yscale('log', base=2)\n"
    "ax.set_yticks(credits)\n"
    "ax.set_yticklabels([str(c) for c in credits])\n"
    "for bar, credit in zip(bars, credits):\n"
    "    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() * 1.1,\n"
    "            str(credit), ha='center', va='bottom', fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

nb1_cells.append(sql_cell("resource_monitor",
    "CREATE OR REPLACE RESOURCE MONITOR partners_monitor\n"
    "    WITH CREDIT_QUOTA = 100\n"
    "    FREQUENCY = MONTHLY\n"
    "    START_TIMESTAMP = IMMEDIATELY\n"
    "    TRIGGERS\n"
    "        ON 75 PERCENT DO NOTIFY\n"
    "        ON 90 PERCENT DO NOTIFY\n"
    "        ON 100 PERCENT DO SUSPEND;"
))

nb1_cells.append(md_cell(
    "✅ **Resultado:**\n"
    "- Query analítica com JOIN de 3 tabelas — resposta sub-segundo\n"
    "- Result Cache — segunda execução instantânea\n"
    "- Resource Monitor — controlo automático de custos\n\n"
    "💡 **Boas práticas de custo:**\n\n"
    "| Prática | Descrição |\n"
    "|---------|-----------|\n"
    "| **Auto-Suspend 60s** | Desliga warehouse após 60s inativo |\n"
    "| **Result Cache** | Reutilização automática (24h, grátis) |\n"
    "| **Multi-cluster** | Escalar para concorrência, não para velocidade |\n"
    "| **Resource Monitors** | Alertas em 75%, suspend em 100% |\n"
    "| **Right-sizing** | XS para dev, M/L para produção |"
))

# --- Final Summary ---
nb1_cells.append(md_cell(
    "---\n"
    "## 🎯 Resumo — O que demonstrámos\n\n"
    "| Capacidade | Valor para o Cliente |\n"
    "|------------|---------------------|\n"
    "| 🏗️ Setup instantâneo | Infraestrutura em segundos, sem tickets |\n"
    "| 📦 Data Loading | Suporte nativo a múltiplos formatos |\n"
    "| 🔄 Snowpipe | Ingestão contínua sem orquestração |\n"
    "| 🔒 Governança | Proteção ao nível dos dados, não da app |\n"
    "| ⚡ Performance | Caching automático, scaling elástico |\n"
    "| 💰 Custos | Pay-per-use + Resource Monitors |\n\n"
    "---\n\n"
    "🔑 **Mensagens-chave:**\n"
    "1. **Separação compute/storage** = escalar sem limites\n"
    "2. **Governança nativa** = conformidade sem código\n"
    "3. **Pay-per-second** = custo previsível e controlável\n"
    "4. **Zero orquestração** = menos infraestrutura para gerir\n\n"
    "**👉 Próximo:** Aprofundamento II — IA, Pipelines Declarativos e Aplicações!"
))


# =============================================================================
# NOTEBOOK 2: Aprofundamento II — IA, Pipelines & Aplicações
# =============================================================================

nb2_cells = []

# Title
nb2_cells.append(md_cell(
    "# 🤖 Aprofundamento II: IA, Pipelines & Aplicações\n"
    "**Snowflake Partner Enablement — Lisboa 2026**\n\n"
    "---\n\n"
    "🎯 **Objetivo:** Demonstrar como o Snowflake transforma dados em insights com IA nativa, "
    "pipelines declarativos e aplicações integradas.\n\n"
    "⏱️ **Duração:** ~30 minutos\n\n"
    "| # | Secção | Tempo | Conceito-chave |\n"
    "|---|--------|-------|----------------|\n"
    "| 1 | 🔄 Dynamic Tables | 8 min | ETL declarativo sem orquestração |\n"
    "| 2 | 🧠 Cortex AI | 12 min | IA nativa em SQL |\n"
    "| 3 | 🤖 Cortex Agent | 5 min | Orquestração multi-ferramenta |\n"
    "| 4 | 📱 Apps & Marketplace | 5 min | Partilha e monetização |\n\n"
    "---\n\n"
    "⚠️ **Pré-requisito:** Este notebook assume que o Aprofundamento I já foi executado "
    "(base de dados, tabelas e dados já existem)."
))

# --- SECTION 1: Dynamic Tables ---
nb2_cells.append(md_cell(
    "---\n"
    "## 1. 🔄 Dynamic Tables — ETL Declarativo\n\n"
    "💡 **Conceito-chave:** Com Dynamic Tables, define-se **O QUÊ** (a transformação) e "
    "o Snowflake gere **O QUANDO** e **O COMO** (refresh automático). ETL tão simples como um SELECT.\n\n"
    "🔑 **Porquê isto importa:** Os clientes gastam 40-60% do tempo de data engineering "
    "em orquestração (Airflow, cron, scripts). Dynamic Tables eliminam essa complexidade por completo.\n\n"
    "```\n"
    "┌────────────────┐     ┌──────────────────────┐     ┌─────────────────┐\n"
    "│  Tabelas RAW   │ ──► │  Dynamic Tables      │ ──► │  Dashboards/BI  │\n"
    "│  (fonte)       │     │  (transformação auto) │     │  (consumo)      │\n"
    "└────────────────┘     └──────────────────────┘     └─────────────────┘\n"
    "         │                        │\n"
    "    Dados chegam           Snowflake mantém\n"
    "    continuamente          tudo atualizado!\n"
    "```\n\n"
    "⚡ `TARGET_LAG = '1 minute'` significa que os dados estarão "
    "atualizados no máximo 1 minuto após a fonte mudar."
))

nb2_cells.append(sql_cell("dt_customer360",
    "CREATE OR REPLACE DYNAMIC TABLE PARTNERS_LISBON_DEMO.ANALYTICS.customer_360\n"
    "    TARGET_LAG = '1 minute'\n"
    "    WAREHOUSE = PARTNERS_WH\n"
    "AS\n"
    "SELECT\n"
    "    c.customer_id,\n"
    "    c.first_name,\n"
    "    c.last_name,\n"
    "    c.email,\n"
    "    c.city,\n"
    "    c.country,\n"
    "    c.region,\n"
    "    c.customer_tier,\n"
    "    COUNT(DISTINCT o.order_id) AS total_orders,\n"
    "    COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 0) AS total_spent,\n"
    "    COALESCE(AVG(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)), 0) AS avg_order_value,\n"
    "    MAX(o.order_date) AS last_order_date,\n"
    "    MODE(p.category) AS favorite_category\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.customers c\n"
    "LEFT JOIN PARTNERS_LISBON_DEMO.RAW.orders o ON c.customer_id = o.customer_id\n"
    "LEFT JOIN PARTNERS_LISBON_DEMO.RAW.order_items oi ON o.order_id = oi.order_id\n"
    "LEFT JOIN PARTNERS_LISBON_DEMO.RAW.products p ON oi.product_id = p.product_id\n"
    "GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.city, c.country, c.region, c.customer_tier;"
))

nb2_cells.append(sql_cell("dt_sales_category",
    "CREATE OR REPLACE DYNAMIC TABLE PARTNERS_LISBON_DEMO.ANALYTICS.sales_by_category\n"
    "    TARGET_LAG = '1 minute'\n"
    "    WAREHOUSE = PARTNERS_WH\n"
    "AS\n"
    "SELECT\n"
    "    p.category,\n"
    "    DATE_TRUNC('month', o.order_date) AS order_month,\n"
    "    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS revenue,\n"
    "    SUM(oi.quantity) AS units_sold,\n"
    "    COUNT(DISTINCT o.order_id) AS num_orders\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.orders o\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.order_items oi ON o.order_id = oi.order_id\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.products p ON oi.product_id = p.product_id\n"
    "GROUP BY p.category, DATE_TRUNC('month', o.order_date);"
))

nb2_cells.append(sql_cell("dt_top_products",
    "CREATE OR REPLACE DYNAMIC TABLE PARTNERS_LISBON_DEMO.ANALYTICS.top_products\n"
    "    TARGET_LAG = '1 minute'\n"
    "    WAREHOUSE = PARTNERS_WH\n"
    "AS\n"
    "SELECT\n"
    "    p.product_id,\n"
    "    p.product_name,\n"
    "    p.category,\n"
    "    p.subcategory,\n"
    "    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS total_revenue,\n"
    "    SUM(oi.quantity) AS total_units_sold,\n"
    "    AVG(r.rating) AS avg_rating,\n"
    "    COUNT(DISTINCT r.review_id) AS num_reviews\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.products p\n"
    "LEFT JOIN PARTNERS_LISBON_DEMO.RAW.order_items oi ON p.product_id = oi.product_id\n"
    "LEFT JOIN PARTNERS_LISBON_DEMO.RAW.product_reviews r ON p.product_id = r.product_id\n"
    "GROUP BY p.product_id, p.product_name, p.category, p.subcategory;"
))

nb2_cells.append(md_cell(
    "### 📊 Consultar as Dynamic Tables\n\n"
    "💡 As Dynamic Tables são consultadas exatamente como tabelas normais. "
    "O Snowflake garante que os dados estão frescos (dentro do TARGET_LAG definido) — "
    "sem precisarmos de acionar nenhum refresh manualmente."
))

nb2_cells.append(sql_cell("dt_top_customers",
    "SELECT first_name, last_name, country, customer_tier, total_orders, total_spent\n"
    "FROM PARTNERS_LISBON_DEMO.ANALYTICS.customer_360\n"
    "ORDER BY total_spent DESC\n"
    "LIMIT 10;"
))

nb2_cells.append(py_cell("viz_top_customers",
    "import matplotlib.pyplot as plt\n\n"
    "df = dt_top_customers.head(10)\n\n"
    "fig, ax = plt.subplots(figsize=(10, 5))\n"
    "names = df['FIRST_NAME'] + ' ' + df['LAST_NAME']\n"
    "bars = ax.barh(names, df['TOTAL_SPENT'], color='#29B5E8')\n"
    "ax.set_title('🏆 Top 10 Clientes por Receita Total', fontsize=14, fontweight='bold')\n"
    "ax.set_xlabel('Total Gasto (€)')\n"
    "ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x:,.0f}'))\n"
    "ax.invert_yaxis()\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

nb2_cells.append(sql_cell("dt_category_totals",
    "SELECT category, SUM(revenue) AS total_revenue\n"
    "FROM PARTNERS_LISBON_DEMO.ANALYTICS.sales_by_category\n"
    "GROUP BY category\n"
    "ORDER BY total_revenue DESC;"
))

nb2_cells.append(py_cell("viz_category_pie",
    "import matplotlib.pyplot as plt\n\n"
    "df = dt_category_totals\n"
    "colors = ['#29B5E8', '#7D44CF', '#FF9F36', '#71D3DC']\n\n"
    "fig, ax = plt.subplots(figsize=(7, 7))\n"
    "wedges, texts, autotexts = ax.pie(\n"
    "    df['TOTAL_REVENUE'],\n"
    "    labels=df['CATEGORY'],\n"
    "    autopct='%1.1f%%',\n"
    "    colors=colors[:len(df)],\n"
    "    textprops={'fontsize': 12}\n"
    ")\n"
    "ax.set_title('📊 Distribuição de Receita por Categoria', fontsize=14, fontweight='bold')\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

nb2_cells.append(md_cell(
    "✅ **Resultado:** 3 Dynamic Tables criadas que:\n"
    "- Agregam dados de múltiplas tabelas automaticamente\n"
    "- Mantêm-se atualizadas sem intervenção manual\n"
    "- São consultadas como tabelas normais\n\n"
    "💡 **Zero Airflow, zero cron, zero orquestração manual.** O Snowflake gere tudo.\n\n"
    "🔑 Se a fonte muda, a DT atualiza automaticamente dentro do TARGET_LAG. "
    "Se **NÃO** muda, **NÃO** consome créditos — eficiência de custos built-in."
))

# --- SECTION 2: Cortex AI ---
nb2_cells.append(md_cell(
    "---\n"
    "## 2. 🧠 Cortex AI — IA Nativa em SQL\n\n"
    "💡 **Conceito-chave:** O Snowflake traz a IA **AOS DADOS**, não o contrário. "
    "Funções de IA chamadas diretamente em SQL — sem APIs externas, sem mover dados, sem infraestrutura ML.\n\n"
    "🔑 **Porquê isto importa:** Qualquer analista SQL pode usar IA — não são precisas equipas de ML "
    "nem integrações complexas. Os dados **NUNCA saem da plataforma** (ideal para dados sensíveis/regulados).\n\n"
    "| Função | O que faz | Exemplo de Uso |\n"
    "|--------|-----------|----------------|\n"
    "| SENTIMENT | Score -1 a 1 | Análise de reviews/NPS |\n"
    "| TRANSLATE | Tradução automática | Localização de conteúdo |\n"
    "| SUMMARIZE | Resumo de texto | Resumos executivos |\n"
    "| CLASSIFY_TEXT | Categorização | Routing de tickets |\n"
    "| COMPLETE | Geração de texto | Marketing, chatbots |"
))

nb2_cells.append(md_cell(
    "### 2.1 📊 Análise de Sentimento\n\n"
    "💡 Numa única query SQL analisamos o sentimento de todas as reviews — "
    "sem Python, sem APIs externas, sem infraestrutura adicional."
))

nb2_cells.append(sql_cell("cortex_sentiment",
    "SELECT\n"
    "    review_id,\n"
    "    product_id,\n"
    "    rating,\n"
    "    LEFT(review_text, 60) AS review_preview,\n"
    "    SNOWFLAKE.CORTEX.SENTIMENT(review_text) AS sentiment_score\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.product_reviews\n"
    "ORDER BY sentiment_score;"
))

nb2_cells.append(py_cell("viz_sentiment",
    "import matplotlib.pyplot as plt\n\n"
    "df = cortex_sentiment\n\n"
    "fig, ax = plt.subplots(figsize=(9, 5))\n"
    "colors = ['#D45B90' if s < 0 else '#FF9F36' if s < 0.5 else '#29B5E8' for s in df['SENTIMENT_SCORE']]\n"
    "ax.bar(df['REVIEW_ID'].astype(str), df['SENTIMENT_SCORE'], color=colors)\n"
    "ax.set_title('🎭 Score de Sentimento por Review', fontsize=14, fontweight='bold')\n"
    "ax.set_xlabel('Review ID')\n"
    "ax.set_ylabel('Sentimento (-1 a 1)')\n"
    "ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)\n"
    "plt.tight_layout()\n"
    "plt.show()"
))

nb2_cells.append(md_cell(
    "### 2.2 🌍 Tradução (Inglês → Português)\n\n"
    "💡 Tradução integrada na plataforma — útil para empresas que recebem feedback em múltiplos idiomas "
    "e precisam de normalizar para análise ou reporting local."
))

nb2_cells.append(sql_cell("cortex_translate",
    "SELECT\n"
    "    review_id,\n"
    "    review_text AS original_en,\n"
    "    SNOWFLAKE.CORTEX.TRANSLATE(review_text, 'en', 'pt') AS traduzido_pt\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.product_reviews\n"
    "LIMIT 5;"
))

nb2_cells.append(md_cell(
    "### 2.3 📝 Sumarização\n\n"
    "💡 Condensar milhares de reviews num único resumo executivo — "
    "ideal para dashboards de produto ou relatórios de satisfação."
))

nb2_cells.append(sql_cell("cortex_summarize",
    "SELECT SNOWFLAKE.CORTEX.SUMMARIZE(\n"
    "    LISTAGG(review_text, '. ') WITHIN GROUP (ORDER BY review_id)\n"
    ") AS summary_of_all_reviews\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.product_reviews;"
))

nb2_cells.append(md_cell(
    "### 2.4 🏷️ Classificação de Texto\n\n"
    "💡 Classificação automática de texto em categorias predefinidas — "
    "imaginem routing automático de tickets de suporte ou categorização de feedback sem regras manuais."
))

nb2_cells.append(sql_cell("cortex_classify",
    "SELECT\n"
    "    review_id,\n"
    "    LEFT(review_text, 50) AS review_preview,\n"
    "    SNOWFLAKE.CORTEX.CLASSIFY_TEXT(\n"
    "        review_text,\n"
    "        ['positive experience', 'negative experience', 'neutral feedback', 'product defect']\n"
    "    ) AS classification\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.product_reviews\n"
    "LIMIT 5;"
))

nb2_cells.append(md_cell(
    "### 2.5 ✨ LLM Completion (Geração de Texto)\n\n"
    "💡 Geração de conteúdo com LLMs (mistral-large2) diretamente via SQL. "
    "Os dados de contexto **NUNCA saem do Snowflake** — ideal para empresas com requisitos de privacidade."
))

nb2_cells.append(sql_cell("cortex_complete",
    "SELECT SNOWFLAKE.CORTEX.COMPLETE(\n"
    "    'mistral-large2',\n"
    "    'Based on these product categories: Electronics, Accessories, Audio, Storage - write a brief 2-sentence marketing tagline for a tech accessories store in Lisbon, Portugal.'\n"
    ") AS generated_text;"
))

nb2_cells.append(md_cell(
    "✅ **Resultado:** 5 funções de IA, todas em SQL puro:\n"
    "- 🎭 Sentimento — quantificar feedback\n"
    "- 🌍 Tradução — localizar conteúdo\n"
    "- 📝 Sumarização — condensar informação\n"
    "- 🏷️ Classificação — categorizar automaticamente\n"
    "- ✨ Geração — criar conteúdo com LLMs\n\n"
    "💡 **Tudo isto sem:** APIs externas, chaves OpenAI, infraestrutura ML, movimento de dados."
))

# --- SECTION 2 continued: Semantic View ---
nb2_cells.append(md_cell(
    "### 2.6 📊 Semantic View — Perguntas em Linguagem Natural\n\n"
    "💡 **Conceito-chave:** A Semantic View cria uma camada semântica que permite ao "
    "Cortex Analyst traduzir perguntas em português/inglês para SQL automaticamente.\n\n"
    "🔑 **Porquê isto importa:** Democratização de dados — qualquer utilizador de negócio "
    "pode obter respostas sem saber SQL."
))

nb2_cells.append(sql_cell("semantic_view",
    "CREATE OR REPLACE SEMANTIC VIEW PARTNERS_LISBON_DEMO.ANALYTICS.sv_sales_analytics\n"
    "    COMMENT = 'Sales analytics semantic view for Partners Lisbon demo'\n"
    "AS SEMANTIC MODEL\n"
    "    TABLES (\n"
    "        cust AS PARTNERS_LISBON_DEMO.RAW.customers PRIMARY KEY (customer_id),\n"
    "        ord AS PARTNERS_LISBON_DEMO.RAW.orders PRIMARY KEY (order_id),\n"
    "        items AS PARTNERS_LISBON_DEMO.RAW.order_items PRIMARY KEY (item_id),\n"
    "        prod AS PARTNERS_LISBON_DEMO.RAW.products PRIMARY KEY (product_id)\n"
    "    )\n"
    "    RELATIONSHIPS (\n"
    "        ord (customer_id) REFERENCES cust (customer_id),\n"
    "        items (order_id) REFERENCES ord (order_id),\n"
    "        items (product_id) REFERENCES prod (product_id)\n"
    "    )\n"
    "    FACTS (\n"
    "        ord.order_count AS COUNT(ord.order_id),\n"
    "        items.total_revenue AS SUM(items.quantity * items.unit_price * (1 - items.discount_pct / 100)),\n"
    "        items.avg_order_value AS AVG(items.quantity * items.unit_price * (1 - items.discount_pct / 100))\n"
    "    )\n"
    "    DIMENSIONS (\n"
    "        cust.country,\n"
    "        cust.region,\n"
    "        cust.customer_tier,\n"
    "        cust.city,\n"
    "        prod.category,\n"
    "        prod.subcategory,\n"
    "        ord.order_status,\n"
    "        ord.order_date\n"
    "    )\n"
    "    METRICS (\n"
    "        monthly_revenue AS SUM(items.quantity * items.unit_price * (1 - items.discount_pct / 100))\n"
    "            GROUP BY DATE_TRUNC('month', ord.order_date)\n"
    "            COMMENT 'Monthly revenue aggregation',\n"
    "        customer_ltv AS SUM(items.quantity * items.unit_price * (1 - items.discount_pct / 100))\n"
    "            GROUP BY cust.customer_id\n"
    "            COMMENT 'Customer lifetime value'\n"
    "    );"
))

nb2_cells.append(md_cell(
    "### 2.7 🔮 ML Functions (Menção Rápida)\n\n"
    "💡 **ML sem código** — o Snowflake treina e serve modelos automaticamente, tudo via SQL:\n\n"
    "| Função | Caso de Uso |\n"
    "|--------|-------------|\n"
    "| `FORECAST` | Previsão de séries temporais |\n"
    "| `ANOMALY_DETECTION` | Deteção de outliers |\n"
    "| `CLASSIFICATION` | Classificação supervisionada |\n"
    "| `TOP_INSIGHTS` | Descoberta automática de padrões |\n\n"
    "Estas funções precisam de mais dados para demonstrar eficazmente, "
    "mas seguem o mesmo princípio: apenas SQL, zero infraestrutura."
))

# --- SECTION 3: Cortex Agent ---
nb2_cells.append(md_cell(
    "---\n"
    "## 3. 🤖 Cortex Agent — Orquestração Multi-Ferramenta\n\n"
    "💡 **Conceito-chave:** O Cortex Agent combina múltiplas capacidades numa única conversa:\n"
    "- 📊 **Cortex Analyst** (text-to-SQL via Semantic View)\n"
    "- 🔍 **Cortex Search** (busca semântica em texto)\n"
    "- 📈 **Data to Chart** (visualização automática)\n\n"
    "🔑 **Porquê isto importa:** Um único agente que responde a perguntas de negócio "
    "combinando dados estruturados E não-estruturados. Qualquer utilizador obtém respostas em segundos.\n\n"
    "⚡ **Passo 1:** Criar um serviço de busca sobre as reviews\n"
    "**Passo 2:** Criar o agente que combina tudo"
))

nb2_cells.append(sql_cell("search_table",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.reviews_for_search AS\n"
    "SELECT\n"
    "    review_id,\n"
    "    product_id,\n"
    "    customer_id,\n"
    "    review_date,\n"
    "    rating,\n"
    "    review_text,\n"
    "    p.product_name,\n"
    "    p.category\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.product_reviews r\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.products p ON r.product_id = p.product_id;"
))

nb2_cells.append(sql_cell("cortex_search",
    "CREATE OR REPLACE CORTEX SEARCH SERVICE PARTNERS_LISBON_DEMO.RAW.reviews_search\n"
    "    ON review_text\n"
    "    ATTRIBUTES rating, product_name, category\n"
    "    WAREHOUSE = PARTNERS_WH\n"
    "    TARGET_LAG = '1 hour'\n"
    "AS (\n"
    "    SELECT review_text, rating, product_name, category\n"
    "    FROM PARTNERS_LISBON_DEMO.RAW.reviews_for_search\n"
    ");"
))

nb2_cells.append(sql_cell("cortex_agent",
    "CREATE OR REPLACE CORTEX AGENT PARTNERS_LISBON_DEMO.ANALYTICS.partners_sales_agent\n"
    "FROM SPECIFICATION $$\n"
    "models:\n"
    "  - mistral-large2\n"
    "orchestration:\n"
    "  agent_type: cortex_analyst_agent\n"
    "instructions: |\n"
    "  You are a sales analytics assistant for a technology products company.\n"
    "  Answer questions about sales, customers, products, and reviews.\n"
    "  Use the analyst tool for structured data queries and search for product reviews.\n"
    "  Always respond in a helpful and concise manner.\n"
    "tools:\n"
    "  - tool_type: cortex_analyst_text_to_sql\n"
    "    tool_spec:\n"
    "      semantic_view: PARTNERS_LISBON_DEMO.ANALYTICS.sv_sales_analytics\n"
    "  - tool_type: cortex_search\n"
    "    tool_spec:\n"
    "      search_service: PARTNERS_LISBON_DEMO.RAW.reviews_search\n"
    "  - tool_type: data_to_chart\n"
    "$$;"
))

nb2_cells.append(md_cell(
    "### 💬 Testar o Agente\n\n"
    "Exemplos de perguntas que podem ser feitas ao agente:\n"
    "- \"Top 5 produtos por receita?\"\n"
    "- \"O que dizem os clientes sobre o laptop?\"\n"
    "- \"Qual a receita por país?\"\n"
    "- \"Mostra-me um gráfico de vendas por categoria\"\n\n"
    "⚡ Podem testar no Snowsight em **AI & ML > Agents**, ou via SQL abaixo:"
))

nb2_cells.append(sql_cell("agent_query",
    "SELECT SNOWFLAKE.CORTEX.AGENT(\n"
    "    'PARTNERS_LISBON_DEMO.ANALYTICS.partners_sales_agent',\n"
    "    'What are the top 3 product categories by total revenue?'\n"
    ") AS agent_response;"
))

nb2_cells.append(md_cell(
    "✅ **Resultado:** Um agente inteligente que:\n"
    "- Traduz perguntas em SQL (via Semantic View)\n"
    "- Pesquisa em texto livre (via Cortex Search)\n"
    "- Gera visualizações (via Data to Chart)\n\n"
    "💡 **Sem infraestrutura adicional.** Tudo gerido pelo Snowflake."
))

# --- SECTION 4: Apps & Marketplace ---
nb2_cells.append(md_cell(
    "---\n"
    "## 4. 📱 Aplicações & Marketplace\n\n"
    "💡 **Conceito-chave:** O Snowflake não é só um data warehouse — é uma plataforma "
    "para partilhar e monetizar dados e aplicações. Zero-copy sharing permite partilhar dados "
    "sem mover bytes. Native Apps permitem empacotar soluções completas.\n\n"
    "🔑 **Porquê isto importa:** O Marketplace é uma oportunidade de **receita recorrente** — "
    "empacotar soluções e distribuí-las globalmente sem infraestrutura de entrega.\n\n"
    "| Funcionalidade | Benefício |\n"
    "|----------------|-----------|\n"
    "| Secure Views | Expor dados sem revelar lógica |\n"
    "| Zero-Copy Clone | Dev/test sem custo de storage |\n"
    "| Tags | Classificação automática |\n"
    "| Native Apps | Solução completa empacotada |\n"
    "| Marketplace | Distribuição global |"
))

nb2_cells.append(md_cell(
    "### 🔐 Secure Views para Partilha\n\n"
    "💡 Uma Secure View expõe dados agregados sem revelar "
    "a lógica de negócio por trás — ideal para partilha com terceiros."
))

nb2_cells.append(sql_cell("secure_view",
    "CREATE OR REPLACE SECURE VIEW PARTNERS_LISBON_DEMO.ANALYTICS.partner_analytics_view AS\n"
    "SELECT\n"
    "    c.country,\n"
    "    c.region,\n"
    "    p.category,\n"
    "    p.subcategory,\n"
    "    COUNT(DISTINCT o.order_id) AS num_orders,\n"
    "    SUM(oi.quantity * oi.unit_price * (1 - oi.discount_pct/100)) AS total_revenue,\n"
    "    AVG(oi.unit_price) AS avg_price\n"
    "FROM PARTNERS_LISBON_DEMO.RAW.customers c\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.orders o ON c.customer_id = o.customer_id\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.order_items oi ON o.order_id = oi.order_id\n"
    "JOIN PARTNERS_LISBON_DEMO.RAW.products p ON oi.product_id = p.product_id\n"
    "GROUP BY c.country, c.region, p.category, p.subcategory;"
))

nb2_cells.append(md_cell(
    "### ♻️ Zero-Copy Cloning\n\n"
    "💡 Clonagem instantânea — cria ambientes de dev/test em milissegundos. "
    "Sem duplicação de dados, sem custo adicional de storage (até haver alterações)."
))

nb2_cells.append(sql_cell("clone_demo",
    "CREATE OR REPLACE TABLE PARTNERS_LISBON_DEMO.RAW.customers_clone\n"
    "    CLONE PARTNERS_LISBON_DEMO.RAW.customers;\n\n"
    "SELECT COUNT(*) AS clone_count FROM PARTNERS_LISBON_DEMO.RAW.customers_clone;"
))

nb2_cells.append(md_cell(
    "### 🏷️ Tags e Classificação de Dados\n\n"
    "💡 Tags permitem classificar dados para governança automática — "
    "por exemplo, aplicar masking automaticamente a TODAS as colunas tagadas como PII."
))

nb2_cells.append(sql_cell("tags_demo",
    "CREATE OR REPLACE TAG PARTNERS_LISBON_DEMO.GOVERNANCE.pii_type\n"
    "    ALLOWED_VALUES 'email', 'phone', 'name', 'address';\n\n"
    "CREATE OR REPLACE TAG PARTNERS_LISBON_DEMO.GOVERNANCE.data_sensitivity\n"
    "    ALLOWED_VALUES 'high', 'medium', 'low';\n\n"
    "ALTER TABLE PARTNERS_LISBON_DEMO.RAW.customers\n"
    "    MODIFY COLUMN email SET TAG PARTNERS_LISBON_DEMO.GOVERNANCE.pii_type = 'email';\n"
    "ALTER TABLE PARTNERS_LISBON_DEMO.RAW.customers\n"
    "    MODIFY COLUMN phone SET TAG PARTNERS_LISBON_DEMO.GOVERNANCE.pii_type = 'phone';\n"
    "ALTER TABLE PARTNERS_LISBON_DEMO.RAW.customers\n"
    "    MODIFY COLUMN email SET TAG PARTNERS_LISBON_DEMO.GOVERNANCE.data_sensitivity = 'high';"
))

nb2_cells.append(sql_cell("show_tags",
    "SELECT *\n"
    "FROM TABLE(INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(\n"
    "    'PARTNERS_LISBON_DEMO.RAW.CUSTOMERS', 'TABLE'\n"
    "));"
))

nb2_cells.append(md_cell(
    "✅ **Resultado:**\n"
    "- 🔐 Secure View — dados partilhados sem expor lógica\n"
    "- ♻️ Clone — ambiente de dev em milissegundos\n"
    "- 🏷️ Tags — classificação para governança automática\n\n"
    "💡 **Oportunidade:**\n"
    "- Criar **Native Apps** com soluções completas\n"
    "- Publicar no **Snowflake Marketplace** (2000+ datasets e apps)\n"
    "- Receita recorrente por consumo"
))

# --- Final Summary ---
nb2_cells.append(md_cell(
    "---\n"
    "## 🎯 Resumo — Aprofundamento II\n\n"
    "| Capacidade | Valor |\n"
    "|------------|---------------------|\n"
    "| 🔄 Dynamic Tables | Pipelines sem orquestração |\n"
    "| 🧠 Cortex AI | IA em SQL, sem infraestrutura |\n"
    "| 🤖 Cortex Agent | Assistentes inteligentes prontos a usar |\n"
    "| 📱 Apps & Marketplace | Escalar soluções globalmente |\n\n"
    "---\n\n"
    "🔑 **Mensagens-chave:**\n"
    "1. **IA nativa** = dados nunca saem da plataforma\n"
    "2. **Pipelines declarativos** = menos código, mais valor\n"
    "3. **Agentes inteligentes** = democratização total de dados\n"
    "4. **Marketplace** = oportunidade de negócio para partners\n\n"
    "**👉 Próximo:** Laboratório Prático — Mãos na massa!"
))


# =============================================================================
# Write notebooks
# =============================================================================

nb1 = make_notebook(nb1_cells)
nb2 = make_notebook(nb2_cells)

output_dir = "/Users/dtinoco/git/partners-lisbon/03_demo_scripts/notebooks"

with open(f"{output_dir}/aprofundamento_I.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb1, f, ensure_ascii=False, indent=2)

with open(f"{output_dir}/aprofundamento_II.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb2, f, ensure_ascii=False, indent=2)

print(f"✅ aprofundamento_I.ipynb  — {len(nb1_cells)} cells")
print(f"✅ aprofundamento_II.ipynb — {len(nb2_cells)} cells")
print("Done!")
