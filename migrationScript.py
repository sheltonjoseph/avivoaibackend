import requests
import mysql.connector
from mysql.connector import Error

def fetch_users(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  
        return response.json().get('users', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []

def insert_data(connection, query, data):
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Error inserting data: {e}")
        return None

def create_tables(cursor):
    try:
        # SQL statements to create tables if they do not exist
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            maiden_name VARCHAR(50),
            age INT,
            gender VARCHAR(10),
            email VARCHAR(100),
            phone VARCHAR(20),
            username VARCHAR(50),
            password VARCHAR(100),
            birth_date DATE,
            image VARCHAR(255),
            blood_group VARCHAR(5),
            height DECIMAL(5,2),
            weight DECIMAL(5,2),
            eye_color VARCHAR(20),
            hair_color VARCHAR(20),
            hair_type VARCHAR(20),
            ip VARCHAR(45),
            mac_address VARCHAR(17),
            university VARCHAR(100),
            ein VARCHAR(20),
            ssn VARCHAR(15),
            user_agent TEXT,
            role VARCHAR(20)
        );
        """

        create_addresses_table = """
        CREATE TABLE IF NOT EXISTS addresses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            address VARCHAR(255),
            city VARCHAR(100),
            state VARCHAR(100),
            state_code VARCHAR(10),
            postal_code VARCHAR(20),
            latitude DECIMAL(10,8),
            longitude DECIMAL(11,8),
            country VARCHAR(100),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            department VARCHAR(100),
            name VARCHAR(100),
            title VARCHAR(100),
            address VARCHAR(255),
            city VARCHAR(100),
            state VARCHAR(100),
            state_code VARCHAR(10),
            postal_code VARCHAR(20),
            latitude DECIMAL(10,8),
            longitude DECIMAL(11,8),
            country VARCHAR(100),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        create_banks_table = """
        CREATE TABLE IF NOT EXISTS banks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            card_expire VARCHAR(10),
            card_number VARCHAR(20),
            card_type VARCHAR(20),
            currency VARCHAR(10),
            iban VARCHAR(34),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        create_crypto_wallets_table = """
        CREATE TABLE IF NOT EXISTS crypto_wallets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            coin VARCHAR(50),
            wallet VARCHAR(255),
            network VARCHAR(50),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """

        # Execute table creation statements
        cursor.execute(create_users_table)
        cursor.execute(create_addresses_table)
        cursor.execute(create_companies_table)
        cursor.execute(create_banks_table)
        cursor.execute(create_crypto_wallets_table)
    except Error as e:
        print(f"Error creating tables: {e}")

def main():
    api_url = "https://dummyjson.com/users"
    users = fetch_users(api_url)

    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='avivodb',
            user='root',
            password='password'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            create_tables(cursor)  

            for user in users:
                user_query = """
                INSERT INTO users (id, first_name, last_name, maiden_name, age, gender, email, phone, username, password, birth_date, image, blood_group, height, weight, eye_color, hair_color, hair_type, ip, mac_address, university, ein, ssn, user_agent, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                user_data = (
                    user['id'], user['firstName'], user['lastName'], user['maidenName'], user['age'], user['gender'],
                    user['email'], user['phone'], user['username'], user['password'], user['birthDate'], user['image'],
                    user['bloodGroup'], user['height'], user['weight'], user['eyeColor'], user['hair']['color'],
                    user['hair']['type'], user['ip'], user['macAddress'], user['university'], user['ein'], user['ssn'],
                    user['userAgent'], user['role']
                )
                insert_data(connection, user_query, user_data)

                address_query = """
                INSERT INTO addresses (user_id, address, city, state, state_code, postal_code, latitude, longitude, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                address_data = (
                    user['id'], user['address']['address'], user['address']['city'], user['address']['state'],
                    user['address']['stateCode'], user['address']['postalCode'], user['address']['coordinates']['lat'],
                    user['address']['coordinates']['lng'], user['address']['country']
                )
                insert_data(connection, address_query, address_data)

                company_query = """
                INSERT INTO companies (user_id, department, name, title, address, city, state, state_code, postal_code, latitude, longitude, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                company_data = (
                    user['id'], user['company']['department'], user['company']['name'], user['company']['title'],
                    user['company']['address']['address'], user['company']['address']['city'],
                    user['company']['address']['state'], user['company']['address']['stateCode'],
                    user['company']['address']['postalCode'], user['company']['address']['coordinates']['lat'],
                    user['company']['address']['coordinates']['lng'], user['company']['address']['country']
                )
                insert_data(connection, company_query, company_data)

                bank_query = """
                INSERT INTO banks (user_id, card_expire, card_number, card_type, currency, iban)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                bank_data = (
                    user['id'], user['bank']['cardExpire'], user['bank']['cardNumber'], user['bank']['cardType'],
                    user['bank']['currency'], user['bank']['iban']
                )
                insert_data(connection, bank_query, bank_data)

                crypto_query = """
                INSERT INTO crypto_wallets (user_id, coin, wallet, network)
                VALUES (%s, %s, %s, %s)
                """
                crypto_data = (
                    user['id'], user['crypto']['coin'], user['crypto']['wallet'], user['crypto']['network']
                )
                insert_data(connection, crypto_query, crypto_data)

            print("Data inserted successfully!")

    except Error as e:
        print(f"Error connecting or inserting data: {e}")

    finally:
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()



 
