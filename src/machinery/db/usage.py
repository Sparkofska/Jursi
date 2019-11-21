import BaseTableManager
import climate
import datetime

tm = climate.ClimateTableManager()
tm.create_table_if_not_exists()

now = datetime.datetime.now()

tm.insert_tuple((str(now), 'test', '24.5', '44.0'))

l = tm.read_all()

for i in l:
    print(i)
