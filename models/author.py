class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.cursor = self.connection.cursor()

        if not self.name:
            raise ValueError("Author name must be specified")
        try:
            self.cursor.execute('INSERT INTO authors (name) VALUES (?)', (self.name,))
            self.connection.commit()
            self.id = self.cursor.lastrowid
        except Exception as e:
            self.connection.rollback()
            print (e)
            raise e

    def __repr__(self):
        return f'<Author {self.name}>'
    
    @property
    def name (self):
        return self.name
    @ name.setter
    def name (self, value):
        if not hasattr(self, '_name'):
            self._name = value

    def articles(self):
        self.cursor.execute("""
            SELECT a.title, m.name
            FROM articles a
            JOIN authors aut ON a.author_id = aut.id
            JOIN magazines m ON a.magazine_id = m.id
            WHERE aut.id = %s
        """, (self.id,))
        return self.cursor.fetchall()
    
    def __delattr__(self):
        self.cursor.close()
        self.connection.close()
      

           