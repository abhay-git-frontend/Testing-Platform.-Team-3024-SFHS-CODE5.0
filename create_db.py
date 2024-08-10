import sqlite3


def create_db():
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("form_data.db")
    cursor = conn.cursor()

    # Create a table for storing form data
    cursor.execute(
        """
       CREATE TABLE form_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    mobile TEXT NOT NULL,
    dob DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
);
    CREATE UNIQUE INDEX idx_email ON form_data (email);
    CREATE UNIQUE INDEX IF NOT EXISTS idx_name ON form_data (name);
    CREATE UNIQUE INDEX IF NOT EXISTS idx_mobile ON form_data (mobile);
        )
    """
    )
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_db()
