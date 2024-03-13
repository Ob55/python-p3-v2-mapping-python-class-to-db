from __init__ import CURSOR, CONN

class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        with CONN:
            CURSOR.execute("""
                CREATE TABLE IF NOT EXISTS departments (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    location TEXT
                )
            """)

    @classmethod
    def drop_table(cls):
        with CONN:
            CURSOR.execute("DROP TABLE IF EXISTS departments")

    def save(self):
        with CONN:
            if self.id is None:
                # Insert new record
                CURSOR.execute("INSERT INTO departments (name, location) VALUES (?, ?)",
                               (self.name, self.location))
                self.id = CURSOR.lastrowid
            else:
                # Update existing record
                CURSOR.execute("UPDATE departments SET name = ?, location = ? WHERE id = ?",
                               (self.name, self.location, self.id))

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    @classmethod
    def get_by_id(cls, department_id):
        CURSOR.execute("SELECT * FROM departments WHERE id = ?", (department_id,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row)

    def delete(self):
        if self.id is not None:
            with CONN:
                CURSOR.execute("DELETE FROM departments WHERE id = ?", (self.id,))

    def update(self):
        if self.id is not None:
            with CONN:
                CURSOR.execute("UPDATE departments SET name = ?, location = ? WHERE id = ?",
                               (self.name, self.location, self.id))
