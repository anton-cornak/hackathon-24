
class Seat:
    def __init__(self, seat_number: int, booked: bool):
        self.seat_number = seat_number
        self.booked = booked

    def __str__(self):
        return f"Seat {self.seat_number} {'booked' if self.booked else 'available'}"

    def to_dict(self):
        return {
            "seat_number": self.seat_number,
            "booked": self.booked
        }

class Floor:
    def __init__(self, floor_number: int, seats: list[Seat]):
        self.floor_number = floor_number
        self.seats = seats


floors = [
    Floor(1, [Seat(101, False), Seat(102, False), Seat(103, False), Seat(104, False)]),
    Floor(2, [Seat(201, False), Seat(202, False), Seat(203, False), Seat(204, False)]),
]


def get_available_seats(floor_number: int) -> list[Seat]:
    floor = next((f for f in floors if f.floor_number == floor_number), None)
    if floor is None:
        return []

    return [seat for seat in floor.seats if not seat.booked]


def book_on_floor(floor_number: int) -> Seat | None:
    floor = next((f for f in floors if f.floor_number == floor_number), None)
    if floor is None:
        return None

    available_seats = [seat for seat in floor.seats if not seat.booked]
    if not available_seats:
        return None

    seat = available_seats[0]
    seat.booked = True

    return seat
