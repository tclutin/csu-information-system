from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Roles(Base):
    __tablename__ = 'roles'

    role_name = Column(Text, primary_key=True)


class Specialty(Base):
    __tablename__ = "specialties"

    specialty_name = Column(Text, primary_key=True)


class Department(Base):
    __tablename__ = "departments"

    department_name = Column(Text, primary_key=True)


class FAQ(Base):
    __tablename__ = 'faq'

    faq_id = Column(BigInteger, primary_key=True)
    question = Column(Text, unique=True, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(BigInteger, primary_key=True)
    short_name = Column(Text, unique=True, nullable=False)
    department = Column(Text, ForeignKey('departments.department_name'), nullable=False)
    specialty = Column(Text, ForeignKey('specialties.specialty_name'), nullable=False)
    user_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)
    department_ref = relationship('Department', backref='groups')
    specialty_ref = relationship('Specialty', backref='groups')


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    username = Column(Text, unique=True, nullable=False)
    role = Column(Text, ForeignKey('roles.role_name'), nullable=False)
    fullname = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=False), nullable=False)

    role_ref = relationship('Roles', backref='users')
