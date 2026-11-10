from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "first_name", "last_name", "address", name="uq_employee_identity"
        ),
    )

    phones = relationship(
        "EmployeePhone", back_populates="employee", cascade="all, delete-orphan"
    )


class EmployeePhone(Base):
    __tablename__ = "employee_phones"

    id = Column(Integer, primary_key=True)

    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)

    phone_number = Column(String, nullable=False)

    employee = relationship("Employee", back_populates="phones")
