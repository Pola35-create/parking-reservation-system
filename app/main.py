from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def root():
    return {"message": "Parking Reservation System API"}