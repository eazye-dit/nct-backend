from flask.ext.login import UserMixin
from sqlalchemy.schema import ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text
# We need to instantiate db and login objects from the nct package.
# They have not yet been defined in __init__.py,
# so this import will fail.
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
    fname = Column(String(30), nullable=False)
    lname = Column(String(30), nullable=False)
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
    fname = Column(String(30), nullable=False)
    lname = Column(String(30), nullable=False)

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

    uid = Column(Integer, ForeignKey(Account.id), primary_key=True)
    rid = Column(Integer, ForeignKey(Role.id), primary_key=True)
    grant_date = Column(DateTime)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    registration = Column(String(11), primary_key=True)
    vin = Column(String(30), nullable=False, unique=True)
    owner = Column(Integer, ForeignKey(Owner.id), nullable=False)
    make = Column(String(30), nullable=False)
    model = Column(String(30), nullable=False)
    year = Column(Integer(4), nullable=False)
    colour = Column(String(20), nullable=False)
    # fuel_type?
    # engine_size?
    # May be defined as an attribute?

class Attribute(db.Model):
    # Attributes that a vehicle can have, such as low rpm, diesel turbo...
    # Car things that I don't know about
    __tablename__ = 'attribute'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class VehicleAttribute(db.Model):
    # Connects Vehicle and Attribute
    __tablename__ = 'vehicle_attribute'

    vid = Column(Integer, ForeignKey(Vehicle.registration), primary_key=True)
    aid = Column(Integer, ForeignKey(Attribute.id), primary_key=True)
    value = Column(String(20))


# TODO: Assignments, test results, and so on
