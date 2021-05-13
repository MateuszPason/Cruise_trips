from DatabaseConnection import *
import SuccessfulNewEntryInDatabaseInfo


class NewPortToDatabase:
    """Fetch primary key value and add new port to database and show new window with information that
     everything is fine"""
    def __init__(self, country, city, capacity):
        cursor.execute('SELECT ports_seq.nextval FROM dual')
        id_increment, = cursor.fetchone()
        get_country_iso = 'SELECT country_iso FROM countries WHERE country_name = :country_name'
        cursor.execute(get_country_iso, country_name=country)
        country_iso, = cursor.fetchone()
        statement = 'INSERT INTO ports (port_id, country_iso, city, capacity) VALUES (:1, :2, :3, :4)'
        cursor.execute(statement, (id_increment, country_iso, city, capacity))
        connection.commit()
        SuccessfulNewEntryInDatabaseInfo.SuccessfulNewPort()


class NewShipToDatabase:
    def __init__(self, ship_name, capacity, port_id):
        cursor.execute('SELECT ships_seq.nextval FROM dual')
        id_increment, = cursor.fetchone()
        statement = 'INSERT INTO ships (ship_id, ship_name, capacity, home_port_id) VALUES (:1, :2, :3, :4)'
        cursor.execute(statement, (id_increment, ship_name, capacity, port_id))
        connection.commit()
        """Add here interface that informs about successful ship add"""
