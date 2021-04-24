from DatabaseConnection import *
import SuccessfulNewEntryInDatabaseInfo


class AddClient:
    def __init__(self, email, first_name, last_name, password, sex, country, phone_number):
        cursor.execute("select clients_id.nextval from dual")
        id_incrementation, = cursor.fetchone()
        get_country_iso = "SELECT country_iso FROM countries WHERE country_name = :country_name"
        cursor.execute(get_country_iso, country_name=country)
        country_iso, = cursor.fetchone()
        statement = 'insert into clients (id, email, first_name, last_name, password, sex, country_iso, phone_number)' \
                    'VALUES (:1, :2, :3, :4, :5, :6, :7, :8)'
        cursor.execute(statement, (id_incrementation, email, first_name, last_name, password, sex, country_iso,
                                   phone_number))
        connection.commit()
        SuccessfulNewEntryInDatabaseInfo.SuccessfulRegister()


class AddEmployee:
    def __init__(self, email, first_name, last_name, phone_number, password, country, register_key):
        cursor.execute("select employees_id.nextval from dual")
        id_incrementation, = cursor.fetchone()
        get_country_iso = "SELECT country_iso FROM countries WHERE country_name = :country_name"
        cursor.execute(get_country_iso, country_name=country)
        country_iso, = cursor.fetchone()
        statement = 'UPDATE employees SET email = :1, employee_id = :2, first_name = :3, last_name = :4,' \
                    'password = :5, country_iso = :6, phone_number = :7 WHERE employee_register_key = :8'
        cursor.execute(statement, (email, id_incrementation, first_name, last_name, password, country_iso,
                                   phone_number, register_key))
        connection.commit()
        SuccessfulNewEntryInDatabaseInfo.SuccessfulRegister()
