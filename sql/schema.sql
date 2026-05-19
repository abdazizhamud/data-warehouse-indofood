-- Create Dimension Tables
CREATE TABLE Dim_Product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    brand VARCHAR(100),
    category VARCHAR(100),
    pack_size VARCHAR(50)
);

CREATE TABLE Dim_Time (
    date_id INT PRIMARY KEY,
    date DATE,
    month INT,
    quarter INT,
    year INT
);

CREATE TABLE Dim_Distributor (
    distributor_id INT PRIMARY KEY,
    distributor_name VARCHAR(255),
    distributor_type VARCHAR(100)
);

CREATE TABLE Dim_Region (
    region_id INT PRIMARY KEY,
    province VARCHAR(100),
    city VARCHAR(100),
    island VARCHAR(100)
);

CREATE TABLE Dim_Promotion (
    promotion_id INT PRIMARY KEY,
    promotion_name VARCHAR(255),
    discount_percentage DECIMAL(5, 2),
    promo_type VARCHAR(100)
);

CREATE TABLE Dim_Customer_Segment (
    segment_id INT PRIMARY KEY,
    segment_name VARCHAR(100)
);

CREATE TABLE Dim_Warehouse (
    warehouse_id INT PRIMARY KEY,
    warehouse_name VARCHAR(255),
    warehouse_location VARCHAR(100)
);

-- Create Fact Table
CREATE TABLE Fact_Sales (
    sales_id INT PRIMARY KEY,
    date_id INT REFERENCES Dim_Time(date_id),
    product_id INT REFERENCES Dim_Product(product_id),
    distributor_id INT REFERENCES Dim_Distributor(distributor_id),
    region_id INT REFERENCES Dim_Region(region_id),
    promotion_id INT REFERENCES Dim_Promotion(promotion_id),
    segment_id INT REFERENCES Dim_Customer_Segment(segment_id),
    warehouse_id INT REFERENCES Dim_Warehouse(warehouse_id),
    quantity INT,
    revenue DECIMAL(15, 2)
);