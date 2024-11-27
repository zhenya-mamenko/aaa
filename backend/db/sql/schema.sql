CREATE TABLE IF NOT EXISTS classes (
  class_id INTEGER PRIMARY KEY,
  class_name VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS categories (
  category_id INTEGER PRIMARY KEY,
  class_id INTEGER NOT NULL,
  category_name VARCHAR(100) NOT NULL UNIQUE,
  FOREIGN KEY (class_id) REFERENCES classes(class_id)
);


CREATE TABLE IF NOT EXISTS assets (
  asset_id INTEGER PRIMARY KEY,
  category_id INTEGER NOT NULL,
  asset_name VARCHAR(250) NOT NULL UNIQUE,
  asset_ticker VARCHAR(10) NOT NULL DEFAULT '',
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);


CREATE TABLE IF NOT EXISTS structures (
  structure_id INTEGER PRIMARY KEY,
  structure_date DATE NOT NULL DEFAULT CURRENT_DATE,
  structure_name VARCHAR(100) NOT NULL UNIQUE,
  is_current BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE IF NOT EXISTS structure_categories (
  structure_id INTEGER NOT NULL,
  category_id INTEGER NOT NULL,
  percentile INTEGER NOT NULL CHECK (percentile > 0 AND percentile < 1000),
  PRIMARY KEY (structure_id, category_id),
  FOREIGN KEY (structure_id) REFERENCES structures(structure_id),
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);


CREATE TRIGGER IF NOT EXISTS structure_categories_insert_check
BEFORE INSERT ON structure_categories
FOR EACH ROW
WHEN (
  (SELECT COALESCE(SUM(percentile), 0)
    FROM structure_categories
    WHERE structure_id = NEW.structure_id
  ) + NEW.percentile > 1000
)
BEGIN
  SELECT RAISE(FAIL, "Structure can't contain categories with sum of percentile > 1000");
END;


CREATE TRIGGER IF NOT EXISTS structure_categories_update_check
BEFORE UPDATE OF percentile ON structure_categories
FOR EACH ROW
WHEN (
  (SELECT COALESCE(SUM(percentile), 0)
    FROM structure_categories
    WHERE structure_id = NEW.structure_id
  ) + NEW.percentile - OLD.percentile > 1000
)
BEGIN
  SELECT RAISE(FAIL, "Structure can't contain categories with sum of percentile > 1000");
END;


CREATE TABLE IF NOT EXISTS assets_values (
  value_id INTEGER PRIMARY KEY AUTOINCREMENT,
  value_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  asset_id INTEGER NOT NULL,
  amount INTEGER NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);


CREATE TABLE IF NOT EXISTS config (
  config_name VARCHAR(50) PRIMARY KEY,
  config_value JSON NOT NULL
);
