import uvicorn
from fastapi import FastAPI

# Create FastAPI app instance
app = FastAPI()


# Define a simple GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# Simple GET path endpoint
@app.get("/hello")
def say_hello():
    return {"message": "Hello, welcome to FastAPI!"}


# Simple POST endpoint that greets the user
@app.post("/greet")
def greet_user(name: str):
    return {"message": "Hello, " + name + "!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
