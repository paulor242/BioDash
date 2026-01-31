class Usuario:
    def __init__(self, db_connection):
        self.db_connection = db_connection
    
    def save(self, nombre, apellido, yoyosq_id=None, encoder_id=None, polea_id=None):
        """Guardar usuario"""
        cursor = self.db_connection.cursor()
        query = """INSERT INTO usuario (nombre, apellido, FK_id_yoyosq, FK_id_encoder, FK_id_polea_conica) 
                   VALUES (%s,%s,%s,%s,%s)"""
        cursor.execute(query, (nombre, apellido, yoyosq_id, encoder_id, polea_id))
        self.db_connection.commit()
        return cursor.lastrowid