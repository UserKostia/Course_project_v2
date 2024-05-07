from .person import Person


class Patient(Person):
    def __init__(self,
                 id: int,
                 name: str,
                 surname: str,
                 middle_name: str,
                 full_name: str,
                 complaint: str,
                 doc_full_name: str,
                 registration_date: str,
                 registration_time: str):
        super().__init__(id, name, surname, middle_name, full_name)
        self._complaint = complaint
        self._doc_full_name = doc_full_name
        self._registration_date = registration_date
        self._registration_time = registration_time

    # def delete_clicked(self, e):
    #     self.task_delete(self)

    def get_complaint(self):
        return self._complaint

    def get_doc_full_name(self):
        return self._doc_full_name

    def get_registration_date(self):
        return self._registration_date

    def get_registration_time(self):
        return self._registration_time

    def set_complaint(self, complaint):
        self._complaint = complaint

    def set_doc_full_name(self, doc_full_name):
        self._doc_full_name = doc_full_name

    def set_registration_date(self, registration_date):
        self._registration_date = registration_date

    def set_registration_time(self, registration_time):
        self._registration_time = registration_time
