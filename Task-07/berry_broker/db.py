import sqlite3
import config

def get_connection():
    conn = sqlite3.connect(config.db_path)
    conn.row_factory = sqlite3.Row
    return conn

def db_initialize():
    conn = get_connection()
    with conn:
        conn.execute("""
        create table if not exists users (
            user_id integer primary key,
            wallet integer default 500,
            bank integer default 0)""")
        conn.execute("""
        create table if not exists items(
            item_id text primary key,
            name text not null,
            cost integer not null,
            description text not null)""")
        conn.execute("""
        create table if not exists inventory(
            id integer primary key autoincrement,
            user_id integer not null,
            item_id text not null,
            qty integer default 1)""")
        conn.execute("""
        create table if not exists history(
            id integer primary key autoincrement,
            user_id integer not null,
            end_id integer,
            action text not null,
            amount integer not null,
            timestamp timestamp default current_timestamp)""")

        items = [
            ('shield', 'Basic wooden shield', 3000, 'Will block the next raid attack'),
            ('gluttony','Normal potion of gluttony', 1000, 'Grants 30% extra loot on your next !setsail.'),
            ('Straw hat', 'A straw hat worn by ********',4000,'gives 10% extra loot and a block on the next turn')
        ]
        conn.executemany("insert or ignore into items values (?,?,?,?)", items)
    conn.close()

def get_user(user_id:int):
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute("select * from users where user_id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            cursor.execute("insert into users (user_id,wallet,bank) values (?,?,?)",
                           (user_id,config.initial_wallet,config.initial_bank))
            cursor.execute("select * from users where user_id=?",(user_id,))
            user =cursor.fetchone()
    conn.close()
    return user