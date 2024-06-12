from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def _init_(self, id, name, category):
        # Initialize a Magazine object with id, name, and category
        self.id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        # Getter for the id property
        return self._id

    @id.setter
    def id(self, value):
        # Setter for the id property, ensuring it's an integer
        if not isinstance(value, int):
            raise ValueError("Magazine ID must be of type int")
        self._id = value

    @property
    def name(self):
        # Getter for the name property
        return self._name

    @name.setter
    def name(self, value):
        # Setter for the name property, ensuring it's a string between 2 and 16 characters
        if not isinstance(value, str):
            raise ValueError("Magazine name must be a string")
        if not (2 <= len(value) <= 16):
            raise ValueError(
                "Magazine name must be between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        # Getter for the category property
        return self._category

    @category.setter
    def category(self, value):
        # Setter for the category property, ensuring it's a non-empty string
        if not isinstance(value, str):
            raise ValueError("Magazine category must be a string")
        if len(value) == 0:
            raise ValueError("Magazine category must not be empty")
        self._category = value

    @staticmethod
    def create(name, category):
        # Create a new Magazine object and insert it into the database
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Insert the magazine into the database
        cursor.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        
        # Commit the changes and retrieve the inserted magazine's ID
        conn.commit()
        magazine_id = cursor.lastrowid
        
        # Close the database connection
        conn.close()
        
        # Return a new Magazine object with the inserted magazine's ID, name and category
        return Magazine(magazine_id, name, category)

    def articles(self):
        # Retrieve all articles associated with this magazine from the database
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Retrieve all articles associated with this magazine from the database
        cursor.execute(
            "SELECT * FROM articles WHERE magazine_id=?", (self.id,))
        
        # Fetch all retrieved articles
        # Retrieve all articles associated with this magazine from the database
        articles = cursor.fetchall()
        
        # Close the database connection
        conn.close()
        
        # Return all articles associated with this magazine from the database
        return articles

    def contributors(self):
        # Retrieve all distinct authors who have contributed to this magazine from the database
        # Establish a database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Retrieve all distinct authors who have contributed to this magazine from the database
        cursor.execute(
            "SELECT DISTINCT authors.* FROM authors INNER JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id=?", (self.id,))
