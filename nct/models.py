from flask.ext.login import UserMixin
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column, Boolean, Integer, String, DateTime, Text
from nct import db, login


@login.user_loader
def get_user(ident):
    return Account.query.get(int(ident))

class Account(db.Model, UserMixin):
    # This is the mechanic/administrator table.
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False)
    password = Column(String(100), nullable=False)
    f_name = Column(String(30), nullable=False)
    l_name = Column(String(30), nullable=False)
    created_on = Column(DateTime, nullable=False)
    last_login = Column(DateTime)

    def get_id(self):
        # Unsure if this function is needed,
        # I thought it might be used for login.user_loader above
        return self.id

class Owner(db.Model):
    # This is the vehicle owner table I suppose
    # A car owner may have more than one car to their name
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True)
    f_name = Column(String(30), nullable=False)
    l_name = Column(String(30), nullable=False)

class Role(db.Model):
    # Roles that an account can have, such as Administrator, Mechanic.
    # Possibility to add other roles.
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)


class AccountRole(db.Model):
    # Connects Account and Role together. Note that an Administrator can also
    # be a Mechanic like this.
    __tablename__ = 'account_role'

    u_id = Column(Integer, ForeignKey(Account.id), primary_key=True)
    r_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
    grant_date = Column(DateTime)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    registration = Column(String(11), primary_key=True)
    vin = Column(String(30), nullable=False, unique=True)
    owner = Column(Integer, ForeignKey(Owner.id), nullable=False)
    make = Column(String(30), nullable=False)
    model = Column(String(30), nullable=False)
    year = Column(Integer, nullable=False)
    colour = Column(String(20), nullable=False)
    # fuel_type?
    # engine_size?
    # May be defined as an attribute?

class Attribute(db.Model):
    # Attributes that a vehicle can have, such as low rpm, diesel turbo...
    # Car things that I don't know about
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

class VehicleAttribute(db.Model):
    # Connects Vehicle and Attribute
    __tablename__ = 'vehicle_attribute'

    registration = Column(String(11), ForeignKey(Vehicle.registration), primary_key=True)
    a_id = Column(Integer, ForeignKey(Attribute.id), primary_key=True)
    value = Column(String(20))


class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    registration = Column(String(11), ForeignKey(Vehicle.registration), nullable=False)
    assigned = Column(Integer, ForeignKey(Account.id), nullable=False)
    is_tested = Column(Boolean, nullable=False)
    date = Column(DateTime, nullable=False)

class Step(db.Model):
    # This is the table that defines each step in the NCT test.
    # Each entry is supposed to be a single step in the test.
    __tablename__ = 'step'

    id = Column(Integer, primary_key=True)
    description = Column(Text, nullable=False) # Method of testing
    notes = Column(Text) # Notes
    name = Column(String(50), nullable=False) # Step name, e.g. "Service Brake Pedal"

class Failure(db.Model):
    # This is a table that defines failures in the NCT test.
    # Each entry is supposed to be a failure connected to a TestStep.
    __tablename__ = 'failure'

    id = Column(Integer, primary_key=True)
    step = Column(Integer, ForeignKey(Step.id), nullable=False)
    item = Column(String(100), nullable=False)
    name = Column(Text, nullable=False)

class TestResult(db.Model):
    # The Result table only defines the points of failure on an appointment.
    # The less returned values from selecting results that match the appointment,
    # the better the test went.
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    appointment = Column(Integer, ForeignKey(Appointment.id), nullable=False)
    failure = Column(Integer, ForeignKey(Failure.id), nullable=False)
