/*
=============================================================================
  SNOWFLAKE PARTNER ENABLEMENT - LISBON
  Script 01: Data Loading
  
  Creates sample e-commerce tables and loads data using INSERT statements.
  Scenario: Online electronics retailer operating in Europe.
  
  Run as: ACCOUNTADMIN
=============================================================================
*/

USE ROLE ACCOUNTADMIN;
USE WAREHOUSE PARTNERS_WH;
USE DATABASE PARTNERS_LISBON_DEMO;
USE SCHEMA RAW;

CREATE OR REPLACE TABLE customers (
    customer_id     INTEGER,
    first_name      VARCHAR(50),
    last_name       VARCHAR(50),
    email           VARCHAR(100),
    phone           VARCHAR(20),
    city            VARCHAR(50),
    country         VARCHAR(50),
    region          VARCHAR(20),
    signup_date     DATE,
    customer_tier   VARCHAR(20)
);

INSERT INTO customers VALUES
(1, 'Joao', 'Silva', 'joao.silva@email.pt', '+351 912 345 678', 'Lisboa', 'Portugal', 'EMEA', '2024-01-15', 'Gold'),
(2, 'Maria', 'Santos', 'maria.santos@email.pt', '+351 923 456 789', 'Porto', 'Portugal', 'EMEA', '2024-02-20', 'Silver'),
(3, 'Pedro', 'Costa', 'pedro.costa@email.pt', '+351 934 567 890', 'Faro', 'Portugal', 'EMEA', '2024-03-10', 'Bronze'),
(4, 'Ana', 'Ferreira', 'ana.ferreira@email.pt', '+351 945 678 901', 'Coimbra', 'Portugal', 'EMEA', '2024-04-05', 'Gold'),
(5, 'Miguel', 'Oliveira', 'miguel.oliveira@email.es', '+34 612 345 678', 'Madrid', 'Spain', 'EMEA', '2024-01-25', 'Silver'),
(6, 'Sofia', 'Rodriguez', 'sofia.rodriguez@email.es', '+34 623 456 789', 'Barcelona', 'Spain', 'EMEA', '2024-05-12', 'Gold'),
(7, 'Hans', 'Mueller', 'hans.mueller@email.de', '+49 151 234 5678', 'Berlin', 'Germany', 'EMEA', '2024-02-28', 'Bronze'),
(8, 'Pierre', 'Dupont', 'pierre.dupont@email.fr', '+33 612 345 678', 'Paris', 'France', 'EMEA', '2024-06-01', 'Silver'),
(9, 'John', 'Smith', 'john.smith@email.com', '+1 212 345 6789', 'New York', 'United States', 'AMER', '2024-03-15', 'Gold'),
(10, 'Sarah', 'Johnson', 'sarah.johnson@email.com', '+1 310 456 7890', 'Los Angeles', 'United States', 'AMER', '2024-04-20', 'Silver'),
(11, 'Carlos', 'Mendes', 'carlos.mendes@email.pt', '+351 956 789 012', 'Braga', 'Portugal', 'EMEA', '2024-07-01', 'Bronze'),
(12, 'Isabella', 'Rossi', 'isabella.rossi@email.it', '+39 331 234 5678', 'Milan', 'Italy', 'EMEA', '2024-05-18', 'Gold'),
(13, 'Yuki', 'Tanaka', 'yuki.tanaka@email.jp', '+81 90 1234 5678', 'Tokyo', 'Japan', 'APJ', '2024-06-15', 'Silver'),
(14, 'Wei', 'Chen', 'wei.chen@email.cn', '+86 138 1234 5678', 'Shanghai', 'China', 'APJ', '2024-07-10', 'Gold'),
(15, 'Emma', 'Wilson', 'emma.wilson@email.co.uk', '+44 7911 123456', 'London', 'United Kingdom', 'EMEA', '2024-08-01', 'Silver');

CREATE OR REPLACE TABLE products (
    product_id      INTEGER,
    product_name    VARCHAR(100),
    category        VARCHAR(50),
    subcategory     VARCHAR(50),
    unit_price      DECIMAL(10,2),
    cost_price      DECIMAL(10,2),
    description     VARCHAR(500)
);

INSERT INTO products VALUES
(101, 'Laptop Pro 15', 'Electronics', 'Laptops', 1299.99, 850.00, 'High-performance laptop with 15-inch display, 16GB RAM, 512GB SSD'),
(102, 'Laptop Air 13', 'Electronics', 'Laptops', 999.99, 650.00, 'Ultra-thin laptop perfect for business professionals'),
(103, 'Wireless Mouse Elite', 'Accessories', 'Mice', 79.99, 35.00, 'Ergonomic wireless mouse with precision tracking'),
(104, 'Mechanical Keyboard Pro', 'Accessories', 'Keyboards', 149.99, 65.00, 'RGB mechanical keyboard with Cherry MX switches'),
(105, 'Monitor UltraWide 34', 'Electronics', 'Monitors', 699.99, 420.00, 'Ultra-wide curved monitor for productivity'),
(106, 'USB-C Hub 7-in-1', 'Accessories', 'Hubs', 59.99, 22.00, 'Multi-port USB-C hub with HDMI, USB 3.0, and SD card reader'),
(107, 'Noise-Cancelling Headphones', 'Audio', 'Headphones', 349.99, 180.00, 'Premium wireless noise-cancelling headphones'),
(108, 'Webcam HD 4K', 'Electronics', 'Cameras', 129.99, 55.00, '4K webcam with auto-focus and built-in microphone'),
(109, 'External SSD 1TB', 'Storage', 'Drives', 119.99, 60.00, 'Portable SSD with USB 3.2 Gen 2 speeds'),
(110, 'Tablet Pro 11', 'Electronics', 'Tablets', 899.99, 580.00, '11-inch tablet with stylus support and keyboard case'),
(111, 'Wireless Charger Pad', 'Accessories', 'Chargers', 39.99, 12.00, 'Fast wireless charging pad for smartphones'),
(112, 'Bluetooth Speaker', 'Audio', 'Speakers', 89.99, 38.00, 'Portable waterproof Bluetooth speaker with 12-hour battery');

CREATE OR REPLACE TABLE orders (
    order_id        INTEGER,
    customer_id     INTEGER,
    order_date      DATE,
    order_status    VARCHAR(20),
    shipping_method VARCHAR(30),
    total_amount    DECIMAL(12,2)
);

INSERT INTO orders VALUES
(1001, 1, '2025-01-05', 'Delivered', 'Express', 1379.98),
(1002, 2, '2025-01-10', 'Delivered', 'Standard', 999.99),
(1003, 3, '2025-01-15', 'Delivered', 'Standard', 229.98),
(1004, 4, '2025-01-20', 'Delivered', 'Express', 2049.97),
(1005, 5, '2025-02-01', 'Delivered', 'Standard', 349.99),
(1006, 6, '2025-02-10', 'Delivered', 'Express', 1949.97),
(1007, 1, '2025-02-15', 'Delivered', 'Express', 699.99),
(1008, 7, '2025-02-20', 'Delivered', 'Standard', 149.99),
(1009, 8, '2025-03-01', 'Delivered', 'Express', 1429.98),
(1010, 9, '2025-03-05', 'Delivered', 'Express', 2199.97),
(1011, 10, '2025-03-10', 'Delivered', 'Standard', 169.98),
(1012, 12, '2025-03-15', 'Delivered', 'Express', 899.99),
(1013, 1, '2025-03-20', 'Delivered', 'Standard', 119.99),
(1014, 4, '2025-04-01', 'Delivered', 'Express', 1349.98),
(1015, 13, '2025-04-05', 'Delivered', 'Standard', 439.98),
(1016, 14, '2025-04-10', 'Delivered', 'Express', 2199.97),
(1017, 2, '2025-04-15', 'Delivered', 'Standard', 89.99),
(1018, 11, '2025-04-20', 'Delivered', 'Express', 79.99),
(1019, 15, '2025-05-01', 'Delivered', 'Express', 1599.97),
(1020, 6, '2025-05-05', 'Shipped', 'Standard', 469.98),
(1021, 3, '2025-05-10', 'Shipped', 'Express', 349.99),
(1022, 9, '2025-05-15', 'Processing', 'Express', 899.99),
(1023, 1, '2025-05-20', 'Processing', 'Standard', 259.98),
(1024, 5, '2025-06-01', 'Processing', 'Express', 1299.99),
(1025, 8, '2025-06-05', 'Processing', 'Standard', 129.99),
(1026, 4, '2025-06-10', 'Pending', 'Express', 799.98),
(1027, 14, '2025-06-15', 'Pending', 'Express', 1949.97),
(1028, 12, '2025-06-20', 'Pending', 'Standard', 239.98),
(1029, 7, '2025-07-01', 'Pending', 'Express', 1299.99),
(1030, 15, '2025-07-05', 'Pending', 'Standard', 449.98);

CREATE OR REPLACE TABLE order_items (
    item_id         INTEGER,
    order_id        INTEGER,
    product_id      INTEGER,
    quantity        INTEGER,
    unit_price      DECIMAL(10,2),
    discount_pct    DECIMAL(5,2)
);

INSERT INTO order_items VALUES
(1, 1001, 101, 1, 1299.99, 0),
(2, 1001, 103, 1, 79.99, 0),
(3, 1002, 102, 1, 999.99, 0),
(4, 1003, 104, 1, 149.99, 0),
(5, 1003, 103, 1, 79.99, 0),
(6, 1004, 101, 1, 1299.99, 0),
(7, 1004, 105, 1, 699.99, 0),
(8, 1004, 106, 1, 59.99, 10),
(9, 1005, 107, 1, 349.99, 0),
(10, 1006, 101, 1, 1299.99, 5),
(11, 1006, 105, 1, 699.99, 5),
(12, 1007, 105, 1, 699.99, 0),
(13, 1008, 104, 1, 149.99, 0),
(14, 1009, 101, 1, 1299.99, 0),
(15, 1009, 108, 1, 129.99, 0),
(16, 1010, 101, 1, 1299.99, 0),
(17, 1010, 110, 1, 899.99, 0),
(18, 1011, 103, 1, 79.99, 0),
(19, 1011, 111, 1, 39.99, 0),
(20, 1011, 106, 1, 59.99, 10),
(21, 1012, 110, 1, 899.99, 0),
(22, 1013, 109, 1, 119.99, 0),
(23, 1014, 101, 1, 1299.99, 0),
(24, 1014, 106, 1, 59.99, 10),
(25, 1015, 107, 1, 349.99, 0),
(26, 1015, 112, 1, 89.99, 0),
(27, 1016, 101, 1, 1299.99, 0),
(28, 1016, 110, 1, 899.99, 0),
(29, 1017, 112, 1, 89.99, 0),
(30, 1018, 103, 1, 79.99, 0),
(31, 1019, 101, 1, 1299.99, 5),
(32, 1019, 107, 1, 349.99, 10),
(33, 1020, 105, 1, 699.99, 5),
(34, 1021, 107, 1, 349.99, 0),
(35, 1022, 110, 1, 899.99, 0),
(36, 1023, 109, 1, 119.99, 0),
(37, 1023, 111, 1, 39.99, 0),
(38, 1023, 106, 1, 59.99, 0),
(39, 1024, 101, 1, 1299.99, 0),
(40, 1025, 108, 1, 129.99, 0),
(41, 1026, 105, 1, 699.99, 0),
(42, 1026, 106, 1, 59.99, 0),
(43, 1027, 101, 1, 1299.99, 5),
(44, 1027, 105, 1, 699.99, 5),
(45, 1028, 104, 1, 149.99, 0),
(46, 1028, 112, 1, 89.99, 0),
(47, 1029, 101, 1, 1299.99, 0),
(48, 1030, 107, 1, 349.99, 0),
(49, 1030, 106, 1, 59.99, 0),
(50, 1030, 111, 1, 39.99, 0);

CREATE OR REPLACE TABLE product_reviews (
    review_id       INTEGER,
    product_id      INTEGER,
    customer_id     INTEGER,
    review_date     DATE,
    rating          INTEGER,
    review_text     VARCHAR(1000)
);

INSERT INTO product_reviews VALUES
(1, 101, 1, '2025-01-20', 5, 'Excellent laptop! Fast performance, great display. Perfect for my data engineering work.'),
(2, 102, 2, '2025-01-25', 4, 'Very lightweight and portable. Battery life could be better but overall a solid machine.'),
(3, 103, 3, '2025-02-01', 3, 'Decent mouse but the scroll wheel feels cheap. Tracking is accurate though.'),
(4, 104, 7, '2025-03-01', 5, 'Best mechanical keyboard I have ever used. The Cherry MX switches are incredibly responsive.'),
(5, 105, 1, '2025-02-28', 5, 'The ultra-wide monitor transformed my productivity. Having multiple windows side by side is amazing.'),
(6, 107, 5, '2025-02-15', 4, 'Great noise cancellation. Comfortable for long use. Sound quality is very good but not audiophile level.'),
(7, 101, 9, '2025-03-20', 5, 'Top-notch laptop. Running complex queries and models without any issue. Highly recommend.'),
(8, 110, 12, '2025-04-01', 4, 'Beautiful tablet with excellent stylus support. A bit heavy compared to competitors.'),
(9, 109, 1, '2025-04-05', 5, 'Blazing fast transfer speeds. The compact design is perfect for carrying between offices.'),
(10, 112, 2, '2025-04-25', 2, 'The speaker sounds okay for the price but the Bluetooth connection keeps dropping. Frustrating.'),
(11, 101, 14, '2025-04-20', 5, 'Incredible performance. Handles all my data analysis workloads effortlessly.'),
(12, 108, 8, '2025-03-15', 4, 'Good image quality for video calls. Auto-focus works well in most lighting conditions.'),
(13, 106, 4, '2025-04-10', 5, 'This hub is exactly what I needed. All ports work perfectly and it is very compact.'),
(14, 107, 15, '2025-05-10', 1, 'Terrible experience. The headphones stopped working after two weeks. Very disappointed with the quality.'),
(15, 111, 10, '2025-03-25', 3, 'Charges slowly compared to wired charger. Works fine but nothing special about it.');

SELECT 'Data loading complete!' AS STATUS;
SELECT 'Customers: ' || COUNT(*) AS ROW_COUNT FROM customers;
SELECT 'Products: ' || COUNT(*) AS ROW_COUNT FROM products;
SELECT 'Orders: ' || COUNT(*) AS ROW_COUNT FROM orders;
SELECT 'Order Items: ' || COUNT(*) AS ROW_COUNT FROM order_items;
SELECT 'Reviews: ' || COUNT(*) AS ROW_COUNT FROM product_reviews;
