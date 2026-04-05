from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")
    password_hash = Column(String)

class Bus(Base):
    __tablename__ = "buses"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    from_city = Column("from", String, index=True)
    to_city = Column("to", String, index=True)
    departureTime = Column(String)
    arrivalTime = Column(String)
    duration = Column(String)
    price = Column(Float)
    totalSeats = Column(Integer)
    availableSeats = Column(Integer)
    bookedSeats = Column(JSON, default=[])
    amenities = Column(JSON, default=[])
    type = Column(String)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(String, primary_key=True, index=True)
    busId = Column(String, ForeignKey("buses.id"))
    busName = Column(String)
    from_city = Column("from", String)
    to_city = Column("to", String)
    date = Column(String)
    seats = Column(JSON, default=[])
    totalPrice = Column(Float)
    passengerName = Column(String)
    passengerEmail = Column(String)
    passengerPhone = Column(String)
    status = Column(String, default="Confirmed")
    bookedAt = Column(String)
