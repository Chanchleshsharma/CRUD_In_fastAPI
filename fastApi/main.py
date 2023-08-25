from fastapi import FastAPI,Depends,HTTPException,Path,Query
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from typing import Optional,Annotated
from starlette import status
from models import Employee
import models
from database import engine,SessionLocal


app=FastAPI()

models.Base.metadata.create_all(bind=engine)



def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy=Annotated[Session,Depends(get_db)]

class Emp(BaseModel):

    emp_name:str = Field( min_length=3,max_length=28)
    dsg:str =Field(min_length=5)
    dep:str =Field(min_length=2,max_length=30)
    sal:int=Field(gt=0)
    city:Optional[str]

    class Config:
        json_schema_extra={
        "example":{
            "emp_name":"Raj",
            "dsg":"abcde",
            "dep":"xyzxyz",
            "sal": 00  ,
            "city":"M.P"    }
        
        }
    


    




# here getting all employee data

@app.get("/emp",status_code=status.HTTP_200_OK)

async def get_records(db:db_dependancy):

    return db.query(Employee).all()
    
# get employee record by id
@app.get("/emp/{emp_id}",status_code=status.HTTP_200_OK)
def get_data_Byid(db:db_dependancy,emp_id:int=Path(gt=0)):
    empdata= db.query(Employee).filter(Employee.id==emp_id).first()
    if  empdata is not None:
        return empdata
    
    raise HTTPException(status_code=404,detail="Employee Not Found")

@app.post("/emp_record",status_code=status.HTTP_201_CREATED)

async def create_emp(db:db_dependancy,emp_request:Emp):

    new_emp=Employee(**emp_request.model_dump())   # here We can also use .dict()
    
    db.add(new_emp)
    db.commit()


@app.put("/emp/update_record/{emp_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_record(db:db_dependancy,emp_record:Emp,emp_id:int =Path(gt=0)):

    updated_data=db.query(Employee).filter(Employee.id==emp_id).first()
    if updated_data is None:
        raise HTTPException(status_code=404,detail="Employee Not Found")
   
    updated_data.emp_name=emp_record.emp_name
    updated_data.dsg=emp_record.dsg
    updated_data.dep=emp_record.dep
    updated_data.sal=emp_record.sal

    updated_data.city=emp_record.city

    db.add(updated_data)
    db.commit()
@app.delete("/emp/delete_record/{emp_id}")
def delet_record(db:db_dependancy,emp_id:int=Path(gt=0)):

    data=db.query(Employee).filter(Employee.id==emp_id).first()
    if data is None:
        raise HTTPException(status_code=404,detail="Invalid Employee Id")
    db.query(Employee).filter(Employee.id==emp_id).delete()
    db.commit()
    # raise HTTPException (status_code=404,detail="Record delete")






