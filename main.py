from fastapi import FastAPI

print(">>> This is the correct file running!")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}

@app.get("/about")
def about():
    return {"message": "You are the best teacher!"}

