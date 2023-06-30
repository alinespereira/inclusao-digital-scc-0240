from db.connection import Connection
from db.data.generator import generate_users, insert_users

def main():
    conn = Connection()
    users = generate_users(200)
    insert_users(users, conn)

if __name__ == '__main__':
    main()
