-- Create database if not exists
create database if not exists lion_parcel;

-- Create dummy table in source if not exists
CREATE TABLE IF NOT EXISTS lion_parcel.retail_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    last_status VARCHAR(100),
    pos_origin VARCHAR(255),
    pos_destination VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);

-- Inject dummy data to source
INSERT INTO lion_parcel.retail_transaction (
    customer_id,
    last_status,
    pos_origin,
    pos_destination,
    deleted_at
)
VALUES
    (12345, 'on_progress', 'jakarta', 'surabaya', NULL),
    (12346, 'done', 'jakarta', 'surabaya', DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 1 HOUR));