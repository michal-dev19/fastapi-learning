import sqlite3

conn = sqlite3.connect("job_board.db")
cursor = conn.cursor()


def init():
    # create tables for job_board if not yet created (foreign keys on!!!)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS driver (id INTEGER PRIMARY KEY, name TEXT, age INT, driving_licence TEXT)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS company (id INTEGER PRIMARY KEY, name TEXT, year_founded INT, industry TEXT, net_worth INT)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS job (id INTEGER PRIMARY KEY, name TEXT, company_id INT, contract TEXT, licence_req TEXT, description TEXT, FOREIGN KEY (company_id) REFERENCES company(id))"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS application (id INTEGER PRIMARY KEY, date_sent TEXT, job_id INT, driver_id INT, open INT, FOREIGN KEY (job_id) REFERENCES job(id), FOREIGN KEY (driver_id) REFERENCES driver(id))"
    )
    cursor.execute("PRAGMA foreign_keys = ON")


init()


def seed():
    # insert data into created tables
    cursor.execute("""
        INSERT INTO driver (name, age, driving_licence) 
        VALUES 
        ('Jim', 34, 'Cat B'), 
        ('Harry', 21, 'Cat B'), 
        ('Brad', 27, 'Cat C')""")

    cursor.execute("""
        INSERT INTO company (name, year_founded, industry, net_worth) 
        VALUES 
        ('Hauling LTD', 2007, 'Transport', 4000000), 
        ('Inpost', 2006, 'Delivery', 20000000), 
        ('Curry''s', 1884, 'Retail', 40000000)""")

    cursor.execute("""
        INSERT INTO job (name, company_id, contract, licence_req, description)
        VALUES 
        ('Retail Assistant', 3, 'Permanent', 'None', 'Help customers around the store'), 
        ('Truck Driver', 1, 'Temporary', 'Category C', 'Transporting fragile cargo across Europe'),
        ('Courier', 2, 'Temporary', 'Category B', 'Deliver parcels to clients across a set region')""")

    cursor.execute("""
        INSERT INTO application (date_sent, job_id, driver_id, open)
        VALUES 
        ('25/05/2026', 1, 2, 1),
        ('11/04/2026', 2, 3, 0)""")
    conn.commit()


seed()
