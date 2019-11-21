
import sqlite3

def print_db_table(tablename, limit = 20):
    
    conn = sqlite3.connect('../jursi.db')
    c = conn.cursor()
    c.execute('SELECT * FROM %s LIMIT %s' % (tablename, limit))
    for row in c:
        print(row)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    
    import sys
    
    if(len(sys.argv) <= 1 or len(sys.argv) > 3):
        print("Wrong number of arguments. Usage: python3 printDbTable <tablename> [<limit>]")
    elif(len(sys.argv) == 2):
        print_db_table(sys.argv[1])
    elif(len(sys.argv) == 3):
        print_db_table(sys.argv[1], sys.argv[2])
