class Person:
    def __init__(self,
                 id: int,
                 name: str,
                 surname: str,
                 middle_name: str,
                 full_name: str):
        self._id = id
        self._name = name
        self._surname = surname
        self._middle_name = middle_name
        self._full_name = full_name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_surname(self):
        return self._surname

    def get_middle_name(self):
        return self._middle_name

    def get_full_name(self):
        return self._full_name

    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def set_surname(self, surname):
        self._surname = surname

    def set_middle_name(self, middle_name):
        self._middle_name = middle_name

    def set_full_name(self, full_name):
        self._full_name = full_name
