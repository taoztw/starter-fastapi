from datetime import datetime
from typing import Optional

from models.wild_oasis.bookings import BookingsBase
from models.wild_oasis.cabins import CabinsRead
from models.wild_oasis.guests import GuestsRead


class BookingsRead(BookingsBase):
    id: str
    cabinId: str
    guestId: str
    created_at: datetime

    cabin: Optional[CabinsRead] = None
    guest: Optional[GuestsRead] = None
