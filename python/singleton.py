import pyodbc as pyodbc

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class DataBase:

    #KONSTRUKTOR
    def __init__(self):
        self.connection_string = ("Driver={ODBC Driver 17 for SQL Server};"
                   "Server= localhost;"
                    "Database=Library;"
                    "Trusted_Connection=yes;")
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()


    #SELECT ALL
    def select_all_items(self):
        self.cursor.execute(f"SELECT * from [dbo].[Users]")
        results = self.cursor.fetchall()
        return results
    
    def select_books_main(self):
        self.cursor.execute(f'SELECT top(25) BookId, Title, Quantity, Img FROM BooksInStock where Quantity != 0')
        results = self.cursor.fetchall()
        return results
    
    def select_book_detail(self, id):
        self.cursor.execute(f"""
        SELECT A.AuthorName, Title, bookDescription, img FROM BooksInStock AS B LEFT JOIN Author as A ON A.AuthorId = B.AuthorID
        where BookID = {id}
        """)
        results = self.cursor.fetchall()
        return results
    
    def data_valid_login(self, password_hash, email):
        self.cursor.execute(f"""
        SELECT FirstName, LastName, PasswordHash, email FROM Users
        where PasswordHash = '{password_hash}' and email = '{email}'
        """)
        results = self.cursor.fetchall()
        return results
    
    
    def select_book_rating(self):
        self.cursor.execute(f"""
        SELECT TOP(3) AVG(R.Rating) as 'average rating', B.Title, A.AuthorName, C.CategoryName FROM Ratings as R
        left join BooksInStock as B ON R.Ratingid = B.RatingId
        left join Users as U ON R.UserId = U.UserId
        left join Category as C ON C.CategoryId = B.CategoryId
        left join Author as A ON A.AuthorId = B.AuthorId
        group by U.FirstName, U.LastName, B.Title, A.AuthorName, C.CategoryName
        """)
        results = self.cursor.fetchall()
        return results
    
    def insert_user(self, first_name, last_name, email, phone, password_hash):
        self.cursor.execute(f"""
        INSERT INTO Users (FirstName, LastName, email, PhoneNumber, PasswordHash) 
        VALUES ('{first_name}', '{last_name}', '{email}', '{phone}', '{password_hash}')
        """)
        self.connection.commit()
        
    def select_search(self, fraze):
        self.cursor.execute(f"select title, bookDescription, img, bookID from BooksInStock where title like '{fraze}%'")
        results = self.cursor.fetchall()
        return results
     
    def select_book_info_order(self, id):
        self.cursor.execute(f"""
        SELECT Img, Title, A.AuthorName FROM BooksInStock AS B
        left join Author as A on A.AuthorId = B.AuthorId
        where BookID = {id}
        """)
        results = self.cursor.fetchall()
        return results