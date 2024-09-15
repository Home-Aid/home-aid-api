# Run command: python src/utils/database/tables.py 

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Enum, Index
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import enum
import pytz
from urllib.parse import quote_plus
# from .. import constants
from src.utils import constants

# Initialize the base class for declarative models
Base = declarative_base()

# Enumerations for specific fields
class ServiceName(enum.Enum):
    cooking = constants.ServiceName.COOKING
    dishWashing = constants.ServiceName.DISH_WASHING
    mopping = constants.ServiceName.MOPPING
    laundry = constants.ServiceName.LAUNDRY

class BookingStatus(enum.Enum):
    pending = constants.BookingStatus.PENDING
    completed = constants.BookingStatus.COMPLETED
    cancelled = constants.BookingStatus.CANCELLED
    refunded = constants.BookingStatus.REFUNDED
    assigned = constants.BookingStatus.ASSIGNED

class PaymentStatus(enum.Enum):
    pending = constants.PaymentStatus.PENDING
    completed = constants.PaymentStatus.COMPLETED
    failed = constants.PaymentStatus.FAILED
    refunded = constants.PaymentStatus.REFUNDED

class PaymentMethod(enum.Enum):
    card = constants.PaymentMethod.CARD
    cash = constants.PaymentMethod.CASH
    upi = constants.PaymentMethod.UPI

# Function to get current time in IST
def current_time_in_IST():
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

# Model Definitions
class Services(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(ServiceName), nullable=False)
    baseCharge = Column(Float, nullable=False)
    baseChargeDescription = Column(String(255), nullable=True)  
    rate = Column(Float, nullable=False)
    rateDescription = Column(String(255), nullable=True)  
    description = Column(String(255), nullable=True)  
    isActive = Column(Boolean, default=True)
    commission = Column(Float, nullable=False)

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    address = Column(String(255), nullable=False)  
    city = Column(String(255), nullable=False)  
    state = Column(String(255), nullable=False)  
    zip = Column(String(20), nullable=False)  
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=current_time_in_IST)
    updatedAt = Column(DateTime, default=current_time_in_IST, onupdate=current_time_in_IST)

    __table_args__ = (
        Index('idx_longitude_latitude', 'longitude', 'latitude'),
        Index('idx_city', 'city'),
    )


class EmployeeSlots(Base):
    __tablename__ = 'employeeSlots'
    id = Column(Integer, primary_key=True, autoincrement=True)
    slot1 = Column(Boolean, default=False)
    slot2 = Column(Boolean, default=False)
    slot3 = Column(Boolean, default=False)
    slot4 = Column(Boolean, default=False)
    slot5 = Column(Boolean, default=False)
    slot6 = Column(Boolean, default=False)
    slot7 = Column(Boolean, default=False)
    slot8 = Column(Boolean, default=False)
    slot9 = Column(Boolean, default=False)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=current_time_in_IST)
    updatedAt = Column(DateTime, default=current_time_in_IST, onupdate=current_time_in_IST)

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  
    email = Column(String(255), nullable=False)  
    phone = Column(String(20), nullable=False)  
    hashedPassword = Column(String(255), nullable=False)  
    addressId = Column(Integer, nullable=False)
    isActive = Column(Boolean, default=True)
    serviceActive = Column(Boolean, default=False)
    morningShift = Column(Boolean, default=False)
    eveningShift = Column(Boolean, default=False)
    cooking = Column(Boolean, default=False)
    dishWashing = Column(Boolean, default=False)
    mopping = Column(Boolean, default=False)
    laundry = Column(Boolean, default=False)

    __table_args__ = (
        Index('idx_addressId', 'addressId'),
    )

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)  
    email = Column(String(255), nullable=False)  
    phone = Column(String(20), nullable=False)  
    hashedPassword = Column(String(255), nullable=False)  
    addressId = Column(Integer, nullable=False)
    isActive = Column(Boolean, default=True)
    
    __table_args__ = (
        Index('idx_addressId', 'addressId'),
    )

class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer, nullable=False)
    status = Column(Enum(BookingStatus), nullable=False)
    paymentStatus = Column(Enum(PaymentStatus), nullable=False)
    total = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)
    tax = Column(Float, nullable=False)
    grandTotal = Column(Float, nullable=False)
    paymentId = Column(Integer, nullable=False)
    createdAt = Column(DateTime, default=current_time_in_IST)
    updatedAt = Column(DateTime, default=current_time_in_IST, onupdate=current_time_in_IST)

    __table_args__ = (
        Index('idx_userId', 'userId'),
    )

class BookingDetails(Base):
    __tablename__ = 'bookingDetails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bookingId = Column(Integer, nullable=False)
    employeeId = Column(Integer, nullable=True)
    serviceName = Column(Enum(ServiceName), nullable=False)
    status = Column(Enum(BookingStatus), nullable=False)
    baseCharge = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    numberOfItems = Column(Integer, nullable=False)
    total = Column(Float, nullable=False)
    createdAt = Column(DateTime, default=current_time_in_IST)
    updatedAt = Column(DateTime, default=current_time_in_IST, onupdate=current_time_in_IST)

    __table_args__ = (
        Index('idx_bookingId', 'bookingId'),
        Index('idx_employeeId', 'employeeId'),
    )

class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    bookingId = Column(Integer, nullable=False)
    paymentMethod = Column(Enum(PaymentMethod), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    createdAt = Column(DateTime, default=current_time_in_IST)
    updatedAt = Column(DateTime, default=current_time_in_IST, onupdate=current_time_in_IST)

    __table_args__ = (
        Index('idx_bookingId', 'bookingId'),
    )

# Configure the Engine & Create All Tables
engine = create_engine('sqlite:///company_services.db')

username = 'root'
password = 'Abcd@1234'
host = 'localhost'
dbname = 'homeaid'

# URL-encode the password
password_encoded = quote_plus(password)
engine = create_engine(f'mysql+pymysql://{username}:{password_encoded}@{host}/{dbname}')

Base.metadata.create_all(engine)


# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session instance
session = Session()

