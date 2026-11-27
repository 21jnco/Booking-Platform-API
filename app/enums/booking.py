import enum

class BookingStatus(str, enum.Enum):
    UNAVAILABLE = "unavailable"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"