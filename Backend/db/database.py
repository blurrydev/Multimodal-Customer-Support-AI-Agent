import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DB_PATH = os.path.join(os.path.dirname(__file__), "crm_mock.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(String, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    item_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    purchase_date = Column(String, nullable=False) # Format: YYYY-MM-DD
    is_final_sale = Column(Boolean, default=False)
    status = Column(String, nullable=False)
    
    customer = relationship("Customer", back_populates="orders")
