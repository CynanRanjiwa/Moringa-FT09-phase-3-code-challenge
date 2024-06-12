from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        # Initialize Magazine with id, name, and category
        self.id = id
        self.name = name
        self.category = category

    # ID property with getter and setter
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("Magazine ID must be an integer")
        self._id = value

    # Name property with getter and setter
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Magazine name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Magazine name must be between 2 and 16 characters")
        self._name = value

    # Category property with getter and setter
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Magazine category must be a string")
        if not value.strip():
            raise ValueError("Magazine category cannot be empty")
        self._category = value

    @staticmethod
    def create(name, category):
        # Insert a new magazine into the database and return a Magazine instance
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the insert command
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        conn.commit()

        # Get the ID of the newly inserted magazine
        magazine_id = cursor.lastrowid

        # Close the connection
        conn.close()

        # Return a new Magazine object
        return Magazine(magazine_id, name, category)

    def get_articles(self):
        # Fetch all articles for this magazine
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the select command
        cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (self.id,))
        articles = cursor.fetchall()

        # Close the connection
        conn.close()

        return articles

    def get_contributors(self):
        # Fetch all distinct authors who have written articles for this magazine
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the select command
        cursor.execute("""
            SELECT DISTINCT authors.* 
            FROM authors 
            JOIN articles ON authors.id = articles.author_id 
            WHERE articles.magazine_id=?
        """, (self.id,))
        contributors = cursor.fetchall()

        # Close the connection
        conn.close()

        return contributors
