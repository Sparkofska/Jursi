from machinery.db.BaseTableManager import BaseTableManager


class ClimateTableManager(BaseTableManager):
    
    TABLE_NAME = "climate"

    _COLNAME_TIMESTAMP = 'timestamp'
    _COLNAME_TAG = 'tag'
    _COLNAME_SENSORTEMPERATURE = 'sensorTemp'
    _COLNAME_SENSORHUMIDITY = 'sensorHumi'
    
    def __init__(self):
        BaseTableManager.__init__(self)
        self.create_table_if_not_exists()
    
    def create_table_if_not_exists(self):
        conn = self.get_db()
        c = conn.cursor()
        c.execute(('''CREATE TABLE IF NOT EXISTS {0} (
            ''' + self._COLNAME_TIMESTAMP + ''' TEXT,
            ''' + self._COLNAME_TAG + ''' TEXT,
            ''' + self._COLNAME_SENSORTEMPERATURE + ''' REAL,
            ''' + self._COLNAME_SENSORHUMIDITY + ''' REAL
            )''').format(self.TABLE_NAME))
        conn.commit()
        self.close_db()
    
    def insert_tuple(self, climate_tuple):
        conn = self.get_db()
        c = conn.cursor()
        
        c.execute('''INSERT INTO %s VALUES
            (?, ?, ?, ?)
            ''' % self.TABLE_NAME, climate_tuple)
        
        conn.commit()
        self.close_db()

    def insert_dict(self, climate_dict):
        tup = (
                climate_dict[self._COLNAME_TIMESTAMP],
                climate_dict[self._COLNAME_TAG],
                climate_dict[self._COLNAME_SENSORTEMPERATURE],
                climate_dict[self._COLNAME_SENSORHUMIDITY]
                ) 
        self.insert_tuple(tup)

    def read_all(self):
        conn = self.get_db()
        c = conn.cursor()
        
        c.execute('''SELECT * FROM %s
            ''' % self.TABLE_NAME)
        
        l = []
        for row in c:
            l.append(self.to_dict(row))
        
        conn.commit()
        self.close_db()
        
        return l
    
    def to_dict(self, climate_tuple):
        return {
                self._COLNAME_TIMESTAMP : climate_tuple[0],
                self._COLNAME_TAG : climate_tuple[1],
                self._COLNAME_SENSORTEMPERATURE : climate_tuple[2],
                self._COLNAME_SENSORHUMIDITY : climate_tuple[3]
                }
    
    
    
    
    
