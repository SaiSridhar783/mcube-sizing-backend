-- drop database mcube_sizing;
-- create database mcube_sizing;
-- use mcube_sizing;
-- Table Creation
CREATE TABLE IF NOT EXISTS role (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS deployment_target (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target_name VARCHAR(50) NOT NULL,
    target_type VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS mcube_component (
    id INT,
    mcube_ver VARCHAR(50),
    component_name TEXT NOT NULL,
    component_ver TEXT NOT NULL,
    component_category TEXT NOT NULL,
    PRIMARY KEY (id, mcube_ver)
);

CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    role_id INT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE IF NOT EXISTS mcube_component_size_slab (
    id INT AUTO_INCREMENT PRIMARY KEY,
    component_id INT NOT NULL,
    price_model_name ENUM('basic', 'standard', 'premium') NOT NULL,
    storage_range TEXT,
    storage INT NOT NULL,
    cpu_range TEXT,
    cpu INT NOT NULL,
    memory_range TEXT,
    memory INT NOT NULL,
    node_range TEXT,
    node_count INT NOT NULL,
    FOREIGN KEY (component_id) REFERENCES mcube_component(id)
);

CREATE TABLE IF NOT EXISTS mcube_estimation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estimation_name TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    created_by INT NOT NULL,
    submitted BOOL DEFAULT false,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS sizing_requirement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estimation_id INT NOT NULL,
    data_vol INT NOT NULL,
    tps_qps INT NOT NULL,
    concurrent_users INT NOT NULL,
    data_retention_period INT NOT NULL,
    max_job_count INT NOT NULL,
    max_report_count INT NOT NULL,
    ai_ml_model INT NOT NULL,
    high_availability BOOL DEFAULT false,
    deployment_type INT NOT NULL,
    location TEXT NOT NULL,
    provided_by INT NOT NULL,
    FOREIGN KEY (estimation_id) REFERENCES mcube_estimation(id),
    FOREIGN KEY (provided_by) REFERENCES user(user_id),
    FOREIGN KEY (deployment_type) REFERENCES deployment_target(id)
);

CREATE TABLE IF NOT EXISTS selected_component (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estimation_id INT,
    size_slab_id INT,
    provided_by INT,
    FOREIGN KEY (size_slab_id) REFERENCES mcube_component_size_slab(id),
    FOREIGN KEY (provided_by) REFERENCES user(user_id)
);

CREATE TABLE IF NOT EXISTS deployment_spec (
    id INT AUTO_INCREMENT PRIMARY KEY,
    estimation_id INT,
    node_id INT,
    node_name TEXT,
    mcube_component_id INT,
    node_type ENUM(
        'master',
        'worker',
        'slave',
        'data',
        'compute',
        'storage'
    ) NOT NULL,
    cpu INT,
    memory INT,
    storage INT,
    target_id INT,
    cost DECIMAL(10, 2),
    FOREIGN KEY (estimation_id) REFERENCES mcube_estimation(id),
    FOREIGN KEY (mcube_component_id) REFERENCES mcube_component(id),
    FOREIGN KEY (target_id) REFERENCES deployment_target(id)
);

-- Table Creation Ends here
------------------------------------------------------------------------------
-- Seed Data
INSERT INTO
    role (name)
VALUES
    ('admin'),
    ('sales'),
    ('architect'),
    ('product'),
    ('infrastructure'),
    ('customer'),
    ('user');

INSERT INTO
    user (name, email, password, role_id)
VALUES
    (
        'Admin User',
        'admin@example.com',
        'password1',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'admin'
        )
    ),
    (
        'Sales User',
        'sales@example.com',
        'password2',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'sales'
        )
    ),
    (
        'Architect User',
        'architect@example.com',
        'password3',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'architect'
        )
    ),
    (
        'Product User',
        'product@example.com',
        'password4',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'product'
        )
    ),
    (
        'Infrastructure User',
        'infrastructure@example.com',
        'password5',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'infrastructure'
        )
    ),
    (
        'Customer User',
        'customer@example.com',
        'password6',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'customer'
        )
    ),
    (
        'Normal User',
        'user@example.com',
        'password7',
        (
            SELECT
                id
            FROM
                role
            WHERE
                name = 'user'
        )
    );

-- Seed Data Ends here