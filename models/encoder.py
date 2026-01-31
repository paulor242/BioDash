class EncoderLineal:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def save(self, data):
        """Guardar datos en tabla encoder_lineal"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO encoder_lineal (
            Force_Max, Velocity_Max_Avg, Velocity_Max, Acceleration_Max, Power_Max,
            Propulsive_Power_avg, Power_Avg, Impulse_Max, Impulse_Avg, Distance_Max,
            Time_Force_Max, Time_impulse, Time_Accel_Max, Ideal_RM, Fatigue
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        values = (
            data.get('force_max'), data.get('velocity_max_avg'), data.get('velocity_max'),
            data.get('acceleration_max'), data.get('power_max'), data.get('propulsive_power_avg'),
            data.get('power_avg'), data.get('impulse_max'), data.get('impulse_avg'),
            data.get('distance_max'), data.get('time_force_max'), data.get('time_impulse'),
            data.get('time_accel_max'), data.get('ideal_rm'), data.get('fatigue')
        )
        cursor.execute(query, values)
        self.db_connection.commit()
        return cursor.lastrowid