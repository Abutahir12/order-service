-- Creating users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255),
    approval_group_id int
);

-- Creating approval table
CREATE TABLE approval_groups (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(255)
);