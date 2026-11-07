import enum

class BookingStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"