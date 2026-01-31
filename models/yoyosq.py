class YoyoSQ:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def save(self, data):
        """Guardar datos en tabla yoyosq"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO yoyosq (
            Acceleration_avg, Acceleration_max, Exentric_power_Max, Exentric_power_Avg,
            Concentric_porwer_max, Consentric_power_Avg, Concentric_Force_max, 
            Concentric_force_Avg, Velocity_Avg, Velocity_max, Exentric_Force_Max, 
            Exentric_Force_Avg
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        values = (
            data.get('acceleration_avg'), data.get('acceleration_max'),
            data.get('exentric_power_max'), data.get('exentric_power_avg'),
            data.get('concentric_power_max'), data.get('concentric_power_avg'),
            data.get('concentric_force_max'), data.get('concentric_force_avg'),
            data.get('velocity_avg'), data.get('velocity_max'),
            data.get('exentric_force_max'), data.get('exentric_force_avg')
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        return cursor.lastrowid