from .person import Person


class Doctor(Person):
    def __init__(self,
                 id: int,
                 name: str,
                 surname: str,
                 middle_name: str,
                 full_name: str,
                 place: str,
                 specialty: str,
                 schedule: dict):
        super().__init__(id, name, surname, middle_name, full_name)
        self._place = place
        self._specialty = specialty
        self._schedule = schedule

    # Геттери для доступу до приватних полів
    def get_place(self):
        return self._place

    def get_specialty(self):
        return self._specialty

    def get_schedule(self):
        return self._schedule

    # Сеттери для зміни приватних полів
    def set_place(self, place):
        self._place = place

    def set_specialty(self, specialty):
        self._specialty = specialty

    def set_schedule(self, schedule):
        self._schedule = schedule
