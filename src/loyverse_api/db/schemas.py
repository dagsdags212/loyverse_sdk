from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import create_engine
from loyverse_api import models
from loyverse_api.core.config import config


class Employee(SQLModel, models.Employee, table=True):
    __tablename__ = "employees"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    receipts: list["Receipt"] = Relationship(back_populates="employee")


class Customer(SQLModel, models.Customer, table=True):
    __tablename__ = "customers"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    receipts: list["Receipt"] = Relationship(back_populates="customer")


class PaymentType(SQLModel, table=True):
    __tablename__ = "payment_types"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    receipts: list["Receipt"] = Relationship(back_populates="payment_type")


class Discount(SQLModel, models.Discount, table=True):
    __tablename__ = "discounts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)


class Receipt(SQLModel, models.Receipt, table=True):
    __tablename__ = "receipts"

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    customer_id: UUID | None = Field(default=None, foreign_key="customers.id")
    customer: Customer = Relationship(back_populates="receipts")
    employee_id: UUID | None = Field(default=None, foreign_key="employees.id")
    employee: Employee = Relationship(back_populates="receipts")
    payment_type_id: UUID | None = Field(default=None, foreign_key="payment_types.id")
    payment_type: PaymentType = Relationship(back_populates="receipts")


def create_database_tables():
    engine = create_engine(config.db_url, echo=True)
    SQLModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database_tables()
