from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class BusBase(BaseModel):
    name: str
    from_city: str = Field(alias="from")
    to_city: str = Field(alias="to")
    departureTime: str
    arrivalTime: str
    duration: str
    price: float
    totalSeats: int
    amenities: List[str]
    type: str
    model_config = ConfigDict(populate_by_name=True)

class BusCreate(BusBase):
    pass

class Bus(BusBase):
    id: str
    availableSeats: int
    bookedSeats: List[int]
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class BookingBase(BaseModel):
    busId: str
    seats: List[int]
    passengerName: str
    passengerEmail: str
    passengerPhone: str
    date: str
    model_config = ConfigDict(populate_by_name=True)

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: str
    busName: str
    from_city: str = Field(alias="from")
    to_city: str = Field(alias="to")
    totalPrice: float
    status: str
    bookedAt: str
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: str
    role: str
    model_config = ConfigDict(from_attributes=True)
