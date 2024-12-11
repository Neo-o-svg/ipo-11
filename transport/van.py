from .vehicle import Vehicle


class Van(Vehicle):
    def __init__(self, is_refrigerated):
        super().__init__()
        self.is_refrigerated = is_refrigerated

    def __str__(self):
        return super().__str__() + f"\nХолодильник: {"есть" if self.is_refrigerated == True else "нету"}"
