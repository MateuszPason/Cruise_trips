import DatabaseConnection


def load_countries_list(fill_combo_box):
    DatabaseConnection.cursor.execute("SELECT country_name FROM countries")
    for i in DatabaseConnection.cursor.fetchall():
        fill_combo_box.addItem(str(i[0]))
