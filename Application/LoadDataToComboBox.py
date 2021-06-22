import DatabaseConnection


def load_countries_list(fill_combo_box):
    DatabaseConnection.cursor.execute("SELECT country_name FROM countries")
    for i in DatabaseConnection.cursor.fetchall():
        fill_combo_box.addItem(str(i[0]))


def load_ports(ships_combobox):
    """Prevents duplicating ports in comboBox"""
    ships_combobox.clear()
    """Get number of rows in ports table"""
    result, = DatabaseConnection.cursor.execute("SELECT COUNT(*) FROM ports").fetchone()

    port_identification = DatabaseConnection.cursor.execute('SELECT country_iso, city FROM ports').fetchall()
    for i in range(result):
        item_to_port_combobox = port_identification[i][0] + ' ' + port_identification[i][1]
        ships_combobox.addItem(item_to_port_combobox)


def load_port_ids(ports_id_combobox):
    ports_id_combobox.clear()
    DatabaseConnection.cursor.execute('SELECT ship_name FROM ships')
    for i in DatabaseConnection.cursor.fetchall():
        ports_id_combobox.addItem(str(i[0]))


def load_ships_available_for_trip(onboard_combobox, port_number):
    onboard_combobox.clear()
    get_all_valid_ships = 'SELECT ship_name FROM ships WHERE home_port_id = :given_port'
    DatabaseConnection.cursor.execute(get_all_valid_ships, given_port=port_number)
    for i in DatabaseConnection.cursor.fetchall():
        onboard_combobox.addItem(str(i[0]))


def load_trips(trips_combobox):
    get_available_trip_names = 'SELECT name FROM trips'
    trips_combobox.clear()
    DatabaseConnection.cursor.execute(get_available_trip_names)
    for i in DatabaseConnection.cursor.fetchall():
        trips_combobox.addItem(str(i[0]))
