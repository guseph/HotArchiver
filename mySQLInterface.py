import mysql.connector
import time

class DBInstance:
    def __init__(self, database):
        
        # Login details are hard-configured to my own mySQL setup on my local machine.
        self.DBinstance = mysql.connector.connect(
            host = "localhost", 
            user = "Inrexis", 
            passwd = "SquareQuoteLong", 
            database = f"{database}"
        )

        self.cursor = self.DBinstance.cursor()

        self.table_name = ''

        self.database_name = database

    def execute_command(self, command):
        try:
            self.cursor.execute(f'{command}')
        except mysql.connector.Error as error:
            print(f'Failed executing command {command}. Error msg: {error}')

    def create_table(self, table_name):
        try:
            self.execute_command('SHOW TABLES')

            if table_name not in self.cursor:
                self.execute_command(f'CREATE TABLE {table_name} (num INT AUTO_INCREMENT PRIMARY KEY, Author varchar(255), CreatedUTC int, ID varchar(7), Score int, Title varchar(1023), URL varchar(255))')
                print(f'Table {table_name} created successfully.')
            else:
                print(f'Table {table_name} already exists.')
        except mysql.connector.Error as error:
            print(f'Failed creating table {table_name}. Error msg: {error}')
    
    def insert_record(self, author, created_utc, sub_id, score, title, url):
        try:
            self.execute_command(f'INSERT INTO {self.table_name} (Author, CreatedUTC, ID, Score, Title, URL) VALUES ({author}, {created_utc}, {sub_id}, {score}, {title}, {url})')
            self.DBinstance.commit()  # commit() is necessary
            print(self.cursor.rowcount, "was inserted successfully.")
        except mysql.connector.Error as error:
            print(f'Failed inserting record {author} {created_utc} {sub_id} {score} {title} {url}. Error msg: {error}')

    
    def insert_many_records(self, table:str, authors:list, created_utcs:list, sub_ids:list, scores:list, titles:list, urls:list):
        try:
            record_pack = [(authors[i], created_utcs[i], sub_ids[i], scores[i], titles[i], urls[i]) for i in range(len(authors))]  # this shouldn't fail

            construct_string = f'INSERT INTO {table} (Author, CreatedUTC, ID, Score, Title, URL) VALUES (%s, %s, %s, %s, %s, %s)'

            self.cursor.executemany(construct_string, record_pack)

            self.DBinstance.commit()  # commit() is necessary

            print(self.cursor.rowcount, "was inserted successfully.")
        except mysql.connector.Error as error:
            print(f'Failed inserting many records. Error msg: {error}. Currently inserted {self.cursor.rowcount} rows.')
    
    def change_table(self, new_table_name):
        try:
            if new_table_name == self.table_name:
                return

            self.execute_command('SHOW TABLES')

            if new_table_name in self.cursor:
                self.table_name = new_table_name
                print(f'Table changed to {self.table_name} successfully.')
                return

            else:
                print(f'Table {new_table_name} does not exist. Creating table.')
                self.create_table(new_table_name)

        except mysql.connector.Error as error:
            print(f'Failed changing table to {new_table_name}. Error msg: {error}')

    def change_database(self, new_DB_name):
        try:
            self.execute_command('SHOW DATABASES')

            if new_DB_name not in self.cursor:
                print(f'Database {new_DB_name} does not exist.')
                return

            self.database_name = new_DB_name
            print(f'Database changed to {new_DB_name} successfully.')

        except mysql.connector.Error as error:
            print(f'Failed changing database to {new_DB_name}. Error msg: {error}')
    
    def clear_table(self, table_name):
        print(f'Clearing table {table_name}.')

        self.execute_command(f'DROP TABLE IF EXISTS {table_name}')
        self.table_name == ''

        print(f'Cleared table {table_name}.')

    
    def delete_record(self, column, col_value):
        self.execute_command("DELETE FROM {self.table_name} WHERE {column} = " + "%s")

        self.cursor.commit() # commit() is necessary