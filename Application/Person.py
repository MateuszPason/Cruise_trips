import AddSomebodyToDatabase


class Person:
    def __init__(self, email, first_name, last_name, password, sex):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.sex = sex


class Client(Person):
    def __init__(self, email, first_name, last_name, password, sex, country, phone_number):
        Person.__init__(self, email, first_name, last_name, password, sex)
        AddSomebodyToDatabase.AddClient(email, first_name, last_name, password, sex, country, phone_number)


