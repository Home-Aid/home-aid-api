DATABASE = "homeaid"
USER_DB = "users"
EMPLOYEE_DB = "employee"

class Database:
    DATABASE = "homeaid"
    
class Tables:
    SERVICES = 'services'
    ADDRESS = 'address'
    EMPLOYEE = 'employee'
    USER = 'users'
    BOOKING = 'booking'
    BOOKING_DETAILS = 'bookingDetails'
    PAYMENTS = 'payments'
    

class ServiceName:
    COOKING = 'cooking'
    DISH_WASHING = 'dishWashing'
    MOPPING = 'mopping'
    LAUNDRY = 'laundry'

class BookingStatus:
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    REFUNDED = 'refunded'
    ASSIGNED = 'assigned'

class PaymentStatus:
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'
    REFUNDED = 'refunded'

class PaymentMethod:
    CARD = 'card'
    CASH = 'cash'
    UPI = 'upi'
