-- Create database if not exists
CREATE DATABASE IF NOT EXISTS lion_parcel;

-- Create dst table for task section
CREATE TABLE IF NOT EXISTS lion_parcel.retail_transaction (
    "id" Int16, 
    "customer_id" Nullable(Int16), 
    "last_status" Nullable(varchar), 
    "pos_origin" Nullable(varchar), 
    "pos_destination" Nullable(varchar), 
    "created_at" DateTime, 
    "updated_at" DateTime, 
    "deleted_at" Nullable(DateTime)
) ENGINE = ReplacingMergeTree ORDER BY id;

-- Create dst table for bonus section
CREATE TABLE IF NOT EXISTS lion_parcel.bonus_json (
    "_id" UUID DEFAULT generateUUIDv4(),
    "id" Nullable(varchar), 
    "runtime_date" Nullable(DateTime), 
    "load_time" Nullable(Float32), 
    "message" Nullable(varchar)
) ENGINE = MergeTree ORDER BY _id;