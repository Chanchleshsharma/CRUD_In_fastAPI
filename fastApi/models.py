from sqlalchemy import Column , Integer, String
from database import Base




class Employee(Base):
    __tablename__='employee'
    id= Column(Integer,primary_key=True,index=True)

    emp_name=Column(String)
    dsg=Column(String)
    dep=Column(String)
    sal=Column(Integer)
    city=Column(String)