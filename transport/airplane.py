from .vehicle import Vehicle


class Airplane(Vehicle):
    def __init__(self, max_altitude):
        super().__init__()
        self.max_altitude = max_altitude

    def load_cargo(self, client):
        super(Airplane, self).load_cargo(client)

    def __str__(self):
        return super().__str__() + f"\nМаксимальная высота полета(в метрах): {self.max_altitude}"
      
