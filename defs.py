import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'database/db.db')

if __name__ == '__main__':
    print(DB_PATH)