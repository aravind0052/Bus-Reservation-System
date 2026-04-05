import uuid
import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bus Reservation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def init_db():
    db = next(get_db())
    if not db.query(models.Bus).first():
        mock_buses = [
            {
                "id": "1", "name": "Vande Bharat Express", "from_city": "Mumbai", "to_city": "Pune",
                "departureTime": "06:00 AM", "arrivalTime": "09:00 AM", "duration": "3h 00m",
                "price": 450, "totalSeats": 40, "availableSeats": 28, "bookedSeats": [3, 7, 12, 15, 18, 22, 25, 30, 33, 36, 38, 40],
                "amenities": ["WiFi", "AC", "USB Charging"], "type": "AC Sleeper"
            },
            {
                "id": "2", "name": "Rajdhani Travels", "from_city": "Delhi", "to_city": "Jaipur",
                "departureTime": "08:00 AM", "arrivalTime": "01:00 PM", "duration": "5h 00m",
                "price": 600, "totalSeats": 40, "availableSeats": 35, "bookedSeats": [1, 5, 10, 20, 31],
                "amenities": ["WiFi", "AC", "Snacks", "Water Bottle"], "type": "Luxury Seater"
            },
            {
                "id": "3", "name": "Kaveri Connect", "from_city": "Bangalore", "to_city": "Chennai",
                "departureTime": "10:00 PM", "arrivalTime": "05:00 AM", "duration": "7h 00m",
                "price": 850, "totalSeats": 40, "availableSeats": 32, "bookedSeats": [2, 4, 8, 14, 19, 27, 34, 39],
                "amenities": ["AC", "Blanket", "Reclining Seats"], "type": "AC Semi-Sleeper"
            },
            {
                "id": "4", "name": "Neeta Tours", "from_city": "Mumbai", "to_city": "Goa",
                "departureTime": "07:30 PM", "arrivalTime": "07:30 AM", "duration": "12h 00m",
                "price": 1200, "totalSeats": 40, "availableSeats": 22, "bookedSeats": [1,2,3,5,6,9,11,13,16,17,21,23,26,28,29,32,35,37],
                "amenities": ["WiFi", "AC", "USB Charging", "Blanket", "Entertainment"], "type": "AC Sleeper"
            },
            {
                "id": "5", "name": "SRS Travels", "from_city": "Hyderabad", "to_city": "Bangalore",
                "departureTime": "09:00 PM", "arrivalTime": "06:00 AM", "duration": "9h 00m",
                "price": 950, "totalSeats": 40, "availableSeats": 38, "bookedSeats": [10, 20],
                "amenities": ["AC", "WiFi", "Water Bottle"], "type": "AC Sleeper"
            },
            {
                "id": "6", "name": "Gujarat Travels", "from_city": "Ahmedabad", "to_city": "Surat",
                "departureTime": "11:00 AM", "arrivalTime": "03:00 PM", "duration": "4h 00m",
                "price": 350, "totalSeats": 40, "availableSeats": 30, "bookedSeats": [1,4,6,8,12,15,22,28,35,40],
                "amenities": ["WiFi", "AC", "USB Charging"], "type": "AC Seater"
            },
            {
                "id": "7", "name": "Royal Cruiser", "from_city": "Kolkata", "to_city": "Patna",
                "departureTime": "08:30 PM", "arrivalTime": "06:30 AM", "duration": "10h 00m",
                "price": 800, "totalSeats": 40, "availableSeats": 10, "bookedSeats": list(range(1, 31)),
                "amenities": ["AC", "Blanket", "Water Bottle"], "type": "AC Sleeper"
            },
            {
                "id": "8", "name": "Intercity SmartBus", "from_city": "Delhi", "to_city": "Lucknow",
                "departureTime": "10:30 PM", "arrivalTime": "06:30 AM", "duration": "8h 00m",
                "price": 999, "totalSeats": 40, "availableSeats": 20, "bookedSeats": list(range(20, 40)),
                "amenities": ["WiFi", "AC", "Blanket", "Snacks"], "type": "Premium Sleeper"
            },
            {
                "id": "9", "name": "Shivneri", "from_city": "Pune", "to_city": "Thane",
                "departureTime": "07:00 AM", "arrivalTime": "10:00 AM", "duration": "3h 00m",
                "price": 500, "totalSeats": 40, "availableSeats": 5, "bookedSeats": list(range(1, 36)),
                "amenities": ["AC", "Water Bottle"], "type": "AC Seater"
            },
            {
                "id": "10", "name": "Chartered Bus", "from_city": "Indore", "to_city": "Bhopal",
                "departureTime": "05:00 PM", "arrivalTime": "09:00 PM", "duration": "4h 00m",
                "price": 400, "totalSeats": 40, "availableSeats": 40, "bookedSeats": [],
                "amenities": ["AC", "WiFi"], "type": "AC Seater"
            }
        ]
        for b in mock_buses:
            bus = models.Bus(**b)
            db.add(bus)

        mock_users = [
            {
                "id": "u-admin", "name": "Admin User", "email": "admin@bus.com",
                "role": "admin", "password_hash": "admin123"
            },
            {
                "id": "u-user", "name": "Test User", "email": "user@example.com",
                "role": "user", "password_hash": "user123"
            }
        ]
        for u in mock_users:
            user = models.User(**u)
            db.add(user)

        db.commit()

@app.get("/api/buses", response_model=List[schemas.Bus])
def get_buses(from_city: Optional[str] = None, to_city: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Bus)
    if from_city:
        query = query.filter(models.Bus.from_city.ilike(f"%{from_city}%"))
    if to_city:
        query = query.filter(models.Bus.to_city.ilike(f"%{to_city}%"))
    return query.all()

@app.get("/api/buses/{bus_id}", response_model=schemas.Bus)
def get_bus(bus_id: str, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

@app.post("/api/book", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == booking.busId).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    
    # Check if seats are already booked
    booked = set(bus.bookedSeats)
    for seat in booking.seats:
        if seat in booked:
            raise HTTPException(status_code=400, detail=f"Seat {seat} is already booked")
            
    # Update bus
    new_booked = list(booked) + booking.seats
    bus.bookedSeats = new_booked
    bus.availableSeats = bus.totalSeats - len(new_booked)
    
    # Create booking
    db_booking = models.Booking(
        id=f"BK-{str(uuid.uuid4()).split('-')[0].upper()}",
        busId=bus.id,
        busName=bus.name,
        from_city=bus.from_city,
        to_city=bus.to_city,
        date=booking.date,
        seats=booking.seats,
        totalPrice=bus.price * len(booking.seats),
        passengerName=booking.passengerName,
        passengerEmail=booking.passengerEmail,
        passengerPhone=booking.passengerPhone,
        status="Confirmed",
        bookedAt=datetime.datetime.utcnow().isoformat() + "Z"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/api/bookings", response_model=List[schemas.Booking])
def get_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).all()

@app.post("/api/login", response_model=schemas.User)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # In a real app, use hashed password comparison like passlib
    if db_user.password_hash != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    return db_user

@app.post("/api/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = models.User(
         id=f"u-{str(uuid.uuid4()).split('-')[0]}",
         name=user.name,
         email=user.email,
         role="user",
         password_hash=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/admin/buses", response_model=schemas.Bus)
def add_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    db_bus = models.Bus(
        id=str(uuid.uuid4()).split('-')[0],
        from_city=bus.from_city,
        to_city=bus.to_city,
        name=bus.name,
        departureTime=bus.departureTime,
        arrivalTime=bus.arrivalTime,
        duration=bus.duration,
        price=bus.price,
        totalSeats=bus.totalSeats,
        availableSeats=bus.totalSeats,
        bookedSeats=[],
        amenities=bus.amenities,
        type=bus.type
    )
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus

@app.delete("/api/admin/buses/{bus_id}")
def delete_bus(bus_id: str, db: Session = Depends(get_db)):
    bus = db.query(models.Bus).filter(models.Bus.id == bus_id).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    db.delete(bus)
    db.commit()
    return {"message": "Bus deleted successfully"}
