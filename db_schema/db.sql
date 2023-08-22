-- Creating users table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    approval_group_id int
);

-- Creating approval table
CREATE TABLE approval_groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(255)
);

-- Creating order table
CREATE TABLE orders (
    order_id VARCHAR(36) PRIMARY KEY,
    order_status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(36) NOT NULL
    updated_at TIMESTAMP,
    updated_by VARCHAR(36)
);