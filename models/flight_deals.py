
class FlightDeals:
    def __init__(self, city: str, iataCode: str, id: int, lowestPrice: int):
        self.city = city
        self.id = id
        self.lowestPrice = lowestPrice
        if iataCode == '':
            self.iataCode = 'TESTING'
        else:
            self.iataCode = iataCode

    def __str__(self):
        return f'city: {self.city} iataCode: {self.iataCode} id: {self.id} lowestPrice: {self.lowestPrice}'

    def to_json(self):
        return {
            'city': self.city,
            'id': self.id,
            'lowestPrice': self.lowestPrice,
            'iataCode': self.iataCode,
        }
