from fastapi import FastAPI,Path,HTTPException,Query
import json 

def load_data():
    with open("patients.json",'r') as f:
        data = json.load(f)
        return data 
     
app = FastAPI()

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

@app.get('/patient')
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