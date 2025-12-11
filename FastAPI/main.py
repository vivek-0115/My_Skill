from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return {
        'message':"Patient Management System API."
    }

@app.get("/about")
def about():
    return {
        'message':"A fully functional API, to manage your patient records."
    }

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patientId}")
def view_patient(patientId: str = Path(..., description="ID of the patient.", example="P002")):
    data = load_data()
    if patientId in data:
        return data[patientId]
    raise HTTPException(status_code=404, detail="Patient Not Found")

@app.get("/sort")
def sort(sort_by: str = Query(..., description="Sort on the basis of Height, Weight & BMI"),
         order: str = Query('asc', description="sort in asc & desc order")):
    
    valid_sortBy = ['height', 'weight', 'bmi']
    if sort_by not in valid_sortBy:
        raise HTTPException(status_code=400, detail=f"Invalid filed, select from {valid_sortBy}")
    
    valid_orders = ['asc', 'desc']
    if order not in valid_orders:
        raise HTTPException(status_code=400, detail=f"Invalid order, select from {valid_orders}")
    
    data = load_data()

    patients = list(data.values())

    reverse_order = True if order == "desc" else False
    sorted_patients = sorted(patients, key=lambda x: x[sort_by], reverse=reverse_order)

    return {
        "sorted_by": sort_by,
        "order": order,
        "total": len(sorted_patients),
        "patients": sorted_patients
    }

    