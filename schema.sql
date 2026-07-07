CREATE TABLE IF NOT EXISTS category(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS menu_item(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL,
    description TEXT,
    price DECIMAL,
    is_available BOOLEAN,
    image_path VARCHAR,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES category(id)
);

CREATE TABLE IF NOT EXISTS restaurant_table(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number INTEGER NOT NULL,
    qr_image_path VARCHAR,
    is_occupied BOOLEAN DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_id INTEGER,
    status VARCHAR DEFAULT 'pending',
    total_amount DECIMAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (table_id) REFERENCES restaurant_table(id)
);

CREATE TABLE IF NOT EXISTS order_item(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity INTEGER NOT NULL,
    price_at_order DECIMAL,
    order_id INTEGER,
    menu_item_id INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_item(id)
);

CREATE TABLE IF NOT EXISTS booking(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name VARCHAR NOT NULL,
    customer_phone VARCHAR,
    date DATE,
    time TIME,
    guests INTEGER NOT NULL,
    status VARCHAR DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    table_id INTEGER,
    FOREIGN KEY (table_id) REFERENCES restaurant_table(id)
);