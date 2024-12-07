from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class BookingCreate(BaseModel):
    patient_name: str
    patient_phone: str
    doctor_id: int
    date: str
    time: str  
    status: str = "confirmed"  


class Booking(BookingCreate):
    id: int 

class BookingUpdate(BaseModel):
    patient_name: Optional[str] = None
    patient_phone: Optional[str] = None
    doctor_id: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    status: Optional[str] = None

bookings: List[Booking] = []
next_booking_id = 1

# 1. 예약 생성
@app.post("/api/bookings", response_model=Booking, status_code=201)
def create_booking(booking: BookingCreate):
    global next_booking_id
    new_booking = Booking(id=next_booking_id, **booking.dict())
    next_booking_id += 1
    bookings.append(new_booking)
    return new_booking

@app.get("/api/bookings", response_model=List[Booking])
def get_bookings(
    doctor_id: Optional[int] = Query(None, description="필터: 의사 ID"),
    date: Optional[str] = Query(None, description="필터: 예약 날짜 (YYYY-MM-DD)")
):
    filtered_bookings = bookings
    if doctor_id:
        filtered_bookings = [b for b in filtered_bookings if b.doctor_id == doctor_id]
    if date:
        filtered_bookings = [b for b in filtered_bookings if b.date == date]
    return filtered_bookings

@app.get("/api/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    booking = next((b for b in bookings if b.id == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@app.put("/api/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, updated_booking: BookingCreate):
    booking = next((b for b in bookings if b.id == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.patient_name = updated_booking.patient_name
    booking.patient_phone = updated_booking.patient_phone
    booking.doctor_id = updated_booking.doctor_id
    booking.date = updated_booking.date
    booking.time = updated_booking.time
    booking.status = updated_booking.status
    return booking

@app.patch("/api/bookings/{booking_id}", response_model=Booking)
def patch_booking(booking_id: int, updates: BookingUpdate):
    booking = next((b for b in bookings if b.id == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(booking, key, value)
    return booking

@app.delete("/api/bookings/{booking_id}", response_model=dict)
def delete_booking(booking_id: int):
    global bookings
    booking = next((b for b in bookings if b.id == booking_id), None)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    bookings = [b for b in bookings if b.id != booking_id]
    return {"message": "Booking deleted successfully"}
