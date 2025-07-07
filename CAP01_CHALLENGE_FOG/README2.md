Simple API with Authentication and Sorting Algorithms
This project demonstrates a simple FastAPI application with user authentication and several endpoints for performing basic operations on lists of numbers. It uses a fake in-memory database for user storage and JWT (JSON Web Tokens) for authentication.

Overview
This API provides the following functionalities:

User Registration and Login: Allows users to register with a username and password, and then log in to receive a JWT access token.
Number Operations (protected by authentication):
Bubble Sort: Sorts a list of numbers.
Even Number Filter: Filters a list to return only even numbers.
Summation: Calculates the sum of a list of numbers.
Maximum Value: Finds the maximum value in a list of numbers.
Binary Search: Searches for a target number in a sorted list.
Average: Calculates the average of a list of numbers.
Files
main.py: Contains the core API logic, including endpoint definitions, authentication functions, and the fake database.
requirements.txt: Lists the project dependencies (FastAPI, Pydantic, Passlib, PyJWT, etc.).
tests.py: Includes unit tests to verify the functionality of the API endpoints.
README.md: The original project description and instructions (you're reading README2.md right now).
Key Features
FastAPI: A modern, high-performance web framework for building APIs with Python.
Pydantic: Used for data validation and schema definition using Python type hints.
Passlib: Provides secure password hashing.
JWT (JSON Web Tokens): Used for user authentication. Users receive a token upon successful login, which must be included in subsequent requests to protected endpoints.
Fake Database: A simple in-memory dictionary simulates a database for user storage. Not suitable for production environments.
Function Explanations (main.py)
register(payload: Credentials): Registers a new user. Hashes the password using get_password_hash() before storing it in fake_db.
login(payload: Credentials): Verifies user credentials against fake_db. If successful, generates and returns a JWT access token using create_access_token().
get_current_user(token): Decodes the JWT and verifies the user's existence in fake_db. Used to protect endpoints.
bubble_sort(payload: Payload, token: str): Implements the Bubble Sort algorithm.
filter_even(payload: Payload, token: str): Filters a list for even numbers.
sum_elements(payload: Payload, token: str): Calculates the sum of numbers in a list.
max_value(payload: Payload, token: str): Finds the maximum value in a list.
binary_search(payload: BinarySearchPayload, token: str): Performs a binary search on a sorted list.
average(payload: Payload, token: str): Calculates the average of numbers in a list.
create_access_token(data: dict): Creates a JWT access token.
get_password_hash(password): Hashes a given password using Passlib.
verify_password(plain_password, hashed_password): Verifies a plain password against a hashed password.
Classes (main.py)
Payload: Pydantic model for endpoints accepting a list of numbers.

class Payload(BaseModel):
    numbers: List[int]

Copy

Apply

BinarySearchPayload: Pydantic model for the binary search endpoint, accepting a list of numbers and a target.

class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int

Copy

Apply

Credentials: Pydantic model for user registration and login, accepting a username and password.

class Credentials(BaseModel):
    username: str
    password: str

Copy

Apply

Authentication Flow
Registration: User sends a POST request to /register with username and password.
Login: User sends a POST request to /login with username and password.
Token Generation: Upon successful login, the server generates a JWT and sends it back to the user.
Protected Endpoints: The user includes the JWT in the token query parameter for all subsequent requests to protected endpoints (e.g., /bubble-sort?token=<JWT>).
Token Verification: The server verifies the JWT using get_current_user().
Running the Application
Create a virtual environment: python3 -m venv venv
Activate the virtual environment: source venv/bin/activate (Linux/macOS) or .\venv\Scripts\activate (Windows)
Install dependencies: pip install -r requirements.txt
Run the application: uvicorn main:app --reload
Running Tests
Ensure the virtual environment is activated.
Run: pytest tests.py
Diagram (Simplified Authentication Flow)
Client <--> /login (POST: username, password) <--> Server (fake_db, JWT generation) <--> Client (receives JWT)
Client <--> /protected-endpoint?token=JWT <--> Server (JWT verification) <--> Client (receives response)