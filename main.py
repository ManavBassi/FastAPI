from fastapi import FastAPI,Path,HTTPException,Query
from typing import Annotated,Literal,Optional
from pydantic import BaseModel,Field, computed_field
from fastapi.responses import JSONResponse
import json 


app = FastAPI()

class Patient(BaseModel):
     id : Annotated[str ,Field(...,description='id of the patient',examples=['P001'])]
     name : Annotated[str , Field(...,description='name of the patient')]
     city : Annotated[str, Field(...,description='city in which patient lived ')]
     age : Annotated[float , Field(...,description='age of the paitent')]
     gender : Annotated[Literal['male','female','others'],Field(...,description='gender of the patient')]
     height : Annotated[float, Field(...,gt=0,description='height of the patient in mtrs')]
     weight : Annotated[float , Field(...,gt = 0,description='weight of the patient in kgs ')]

     @computed_field
     @property
     def bmi(self) -> float:
         bmi = round(self.weight/(self.height**2),2)
         return bmi 
     
     @computed_field
     @property
     def verdict(self) -> str:
         if self.bmi < 18.5:
             return 'Underweight'
         elif self.bmi <25:
             return 'Normal'
         elif self.bmi < 30 :
             return 'Normal'
         else:
             return 'Obese'

def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('patients.json','w')as f:
        json.dump(data,f)       

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}

@app.get("/about")
def about():
    return {"message": "You are the best teacher!"}

@app.get("/view")
def view():
    print(">>> /view route loaded successfully!")
    data = load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id:str = Path(...,description='id of patient in db',example='P001')):
    data  =  load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail = 'patient not found')

@app.get('/sort')
def patient_view(sort_by:str = Query(...,description='sort on basis of height,weight or bmi'),order:str = Query('asc',description ='order on basis of asc,desc')):
    
    valid_field = ['height','weight','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code = 400,detail = 'valid field not found')
    if order not in ['asc','desc']:
        raise HTTPException(status_code = 400,detail = 'valid order not found')
    
    data = load_data()
    sort_order = True if order =='desc' else False
    sorted_data = sorted(data.values(),key  = lambda x: x.get(sort_by,0), reverse = sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient : Patient):
    
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code = 400, detail = 'patient already exists')
    data[patient.id] = patient.model_dump(exclude = ['id'])

    save_data(data)

    return JSONResponse(status_code = 201, content  = {'message': 'patient created sucessfully'})
    