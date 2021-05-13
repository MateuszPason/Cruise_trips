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

    """Load all ports that user can modify"""
    port_identification = DatabaseConnection.cursor.execute('SELECT country_iso, city FROM ports').fetchall()
    for i in range(result):
        item_to_port_combobox = port_identification[i][0] + ' ' + port_identification[i][1]
        ships_combobox.addItem(item_to_port_combobox)
