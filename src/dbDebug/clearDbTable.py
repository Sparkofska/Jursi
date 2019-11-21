
import sqlite3

def clear_db_table(tablename):
    
    conn = sqlite3.connect('../jursi.db')
    c = conn.cursor()
    c.execute('DELETE FROM %s' % (tablename,))
    for row in c:
        print(row)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    
    import sys
    
    if(len(sys.argv) <= 1 or len(sys.argv) > 2):
        print("Wrong number of arguments. Usage: python3 printDbTable <tablename> [<limit>]")
    elif(len(sys.argv) == 2):
        clear_db_table(sys.argv[1])
