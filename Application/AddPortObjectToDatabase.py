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
    """Fetch primary key value for ship and add new ship to database"""
    def __init__(self, ship_name, capacity, port_id):
        cursor.execute('SELECT ships_seq.nextval FROM dual')
        id_increment, = cursor.fetchone()
        statement = 'INSERT INTO ships (ship_id, ship_name, capacity, home_port_id) VALUES (:1, :2, :3, :4)'
        cursor.execute(statement, (id_increment, ship_name, capacity, port_id))

        for i in range(1, capacity+1):
            cursor.execute('SELECT ship_cabins_seq.nextval FROM dual')
            cabin_id, = cursor.fetchone()
            statement = 'INSERT INTO ship_cabins (ship_cabin_id, ship_id, room_number) VALUES (:1, :2, :3)'
            cursor.execute(statement, (cabin_id, id_increment, i))
        connection.commit()
        SuccessfulNewEntryInDatabaseInfo.SuccessfulNewShip()


class NewShipCabinToDatabase:
    """Add new ship cabin to database, based on data passed by CEO"""
    def __init__(self, ship_name, room_number, room_type, number_of_guests, sq_m_cabin, sq_m_balcony):
        get_ship_id = 'SELECT ship_id FROM ships WHERE ship_name = :given_name'
        cursor.execute(get_ship_id, given_name=ship_name)
        ship_id, = cursor.fetchone()
        statement = 'UPDATE ship_cabins SET room_type = :1, guests = :2, sq_m = :3, balcony_sq_m = :4' \
                    'WHERE ship_id = :5 AND room_number = :6'
        cursor.execute(statement, (room_type, number_of_guests, sq_m_cabin, sq_m_balcony, ship_id, room_number))
        connection.commit()
        SuccessfulNewEntryInDatabaseInfo.SuccessfulNewShipCabin()


class NewTripToDatabase:
    """Add new trip with details passed by port manager"""
    def __init__(self, trip_name, trip_price, ship_name, start_date, end_date, port_number):
        cursor.execute('SELECT trip_seq.nextval FROM dual')
        trip_id, = cursor.fetchone()
        get_leaving_country_iso = 'SELECT country_iso FROM ports WHERE port_id = :given_port_id'
        cursor.execute(get_leaving_country_iso, given_port_id=port_number)
        country_iso, = cursor.fetchone()
        get_country_name = 'SELECT country_name FROM countries WHERE country_iso = :given_iso'
        cursor.execute(get_country_name, given_iso=country_iso)
        country_name, = cursor.fetchone()
        get_leaving_city = 'SELECT city FROM ports WHERE port_id = :given_port_id'
        cursor.execute(get_leaving_city, given_port_id=port_number)
        leaving_city, = cursor.fetchone()
        insert_trip_details = "INSERT INTO trips (trip_id, name, price, leaving_from_country, leaving_from_city," \
                              " start_date, end_date, onboard) VALUES (:1, :2, :3, :4, :5, TO_DATE(:6, 'DD/MM/YYYY')," \
                              " TO_DATE(:7, 'DD/MM/YYYY'), :8)"
        cursor.execute(insert_trip_details, (trip_id, trip_name, trip_price, country_name, leaving_city, start_date,
                                             end_date, ship_name))
        connection.commit()

        """This email is used to reload used account after successful trip add"""
        get_email = 'SELECT email FROM employees WHERE port_id = :given_port_id'
        cursor.execute(get_email, given_port_id=port_number)
        emp_email, = cursor.fetchone()
        SuccessfulNewEntryInDatabaseInfo.SuccessfulNewTrip(emp_email)
