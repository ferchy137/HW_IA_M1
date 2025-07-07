from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt

fake_db = {"users": {}}

app = FastAPI()

"""
Payload model representing a collection of integers.

Attributes:
    numbers (List[int]): A list of integer values to be processed or validated.
"""
class Payload(BaseModel):
    numbers: List[int]

"""
BinarySearchPayload is a data model for binary search operations.

Attributes:
    numbers (List[int]): A list of integers to search within.
    target (int): The integer value to search for in the list.
"""
class BinarySearchPayload(BaseModel):
    numbers: List[int]
    target: int


# Fake db
fake_db = {"users": {}}

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmcifQ.trzFhzluB4v-i9JYDW1U9U-8ySWl276asroaKX0mjjo"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


# Aplicacion
app = FastAPI()


class Credentials(BaseModel):
    username: str
    password: str


# Endpoint de registro, guarda clave encriptada
    """
    Register a new user with the given credentials.
        
    This endpoint handles user registration by:
    - Checking if the username already exists
    - Hashing the provided password
    - Storing the user in the fake database
        
    Args:
        payload (Credentials): User registration credentials containing username and password
        
    Returns:
        dict: A message confirming successful user registration
        
    Raises:
        HTTPException: 400 error if username already exists
    """
@app.post("/register")
def register(payload: Credentials): 
    username = payload.username
    password = payload.password

    if username in fake_db["users"].keys():
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = get_password_hash(password)
    fake_db["users"][username] = {"password": hashed_password}
    return {"message": "User registered successfully"}
    
    # Endpoint de login, devuelve token
    """
    Authenticate a user and generate an access token.

    This endpoint handles user login by:
    - Verifying the provided username exists
    - Validating the password
    - Generating and returning an access token for authenticated users

    Args:
    payload (Credentials): User login credentials containing username and password

    Returns:
    dict: An access token for the authenticated user

    Raises:
    HTTPException: 401 error if credentials are invalid
    """
@app.post("/login")
def login(payload: Credentials):
    username = payload.username
    password = payload.password

    if username not in fake_db["users"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = fake_db["users"][username]
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token}


# Función para verificar token
    """
    Validate and extract the current user from a JWT token.
    
    Decodes the provided token and checks its validity by:
    - Verifying the token's signature using the SECRET_KEY
    - Ensuring the token contains a valid username
    - Confirming the username exists in the user database
    
    Args:
        token (str): JWT authentication token
    
    Returns:
        str: Username extracted from the token
    
    Raises:
        HTTPException: 401 error if token is invalid or user does not exist
    """
def get_current_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        if username not in fake_db["users"].keys():
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        return username
    except:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


# Bubble Sort
    """
    Endpoint for sorting a list of numbers using the Bubble Sort algorithm.

    Requires a valid authentication token and a payload containing a list of numbers.
    Returns the sorted list of numbers.

    Args:
        payload (Payload): A payload object containing a list of numbers to be sorted
        token (str): Authentication token for validating user access

    Returns:
        dict: A dictionary with the sorted list of numbers under the key "numbers"
    """
@app.post("/bubble-sort")
def bubble_sort(payload: Payload, token: str):
    """
    Recibe una lista de números y devuelve la lista ordenada utilizando el algoritmo de Bubble Sort.
    """
    get_current_user(token)  # Verify token
    numbers = payload.numbers
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return {"numbers": numbers}


# Filtro de Pares
    """
    Endpoint for filtering even numbers from a list.

    Requires a valid authentication token and a payload containing a list of numbers.
    Returns a list of only the even numbers.

    Args:
        payload (Payload): A payload object containing a list of numbers to be filtered
        token (str): Authentication token for validating user access

    Returns:
        dict: A dictionary with the filtered even numbers under the key "even_numbers"
    """
@app.post("/filter-even")
def filter_even(payload: Payload, token: str):
    get_current_user(token)
    numbers = payload.numbers
    even_numbers = [number for number in numbers if number % 2 == 0]
    return {"even_numbers": even_numbers}


# Suma de Elementos
    """
    Endpoint for calculating the sum of elements in a list of numbers.

    Requires a valid authentication token and a payload containing a list of numbers.
    Returns the sum of all numbers in the list.

    Args:
        payload (Payload): A payload object containing a list of numbers to be summed
        token (str): Authentication token for validating user access

    Returns:
        dict: A dictionary with the sum of numbers under the key "sum"
    """
@app.post("/sum-elements")
def sum_elements(payload: Payload, token: str):
    get_current_user(token)
    numbers = payload.numbers
    return {"sum": sum(numbers)}


# Máximo Valor
    """
    Endpoint to calculate the maximum value from a list of numbers.

    Args:
        payload (Payload): The request body containing a list of numbers.
        token (str): The authentication token provided by the user.

    Returns:
        dict: A dictionary containing the maximum value from the provided list of numbers, with the key 'max'.

    Raises:
        HTTPException: If the user is not authenticated or authorized.
    """
@app.post("/max-value")
def max_value(payload: Payload, token: str):
    get_current_user(token)
    numbers = payload.numbers
    return {"max": max(numbers)}


# Búsqueda Binaria
    """
    Performs a binary search on a sorted list of numbers to find a target value.

    Args:
        payload (BinarySearchPayload): An object containing:
            - numbers (List[int]): A sorted list of integers to search.
            - target (int): The integer value to search for in the list.
        token (str): Authentication token for the current user.

    Returns:
        dict: A dictionary with:
            - "found" (bool): True if the target is found in the list, False otherwise.
            - "index" (int): The index of the target in the list if found, otherwise -1.

    Raises:
        HTTPException: If the user is not authenticated.

    Example:
        Request payload:
            {
                "numbers": [1, 3, 5, 7, 9],
                "target": 5
            }
        Response:
            {
                "found": True,
                "index": 2
            }
    """
@app.post("/binary-search")
def binary_search(payload: BinarySearchPayload, token: str):
    get_current_user(token)

    numbers = payload.numbers
    target = payload.target

    left, right = 0, len(numbers) - 1
    while left <= right:
        mid = (left + right) // 2
        if numbers[mid] == target:
            return {"found": True, "index": mid}
        elif numbers[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return {"found": False, "index": -1}


# Endpoint to calculate the average of a list of numbers

"""
Calculates the average of a list of numbers.

Args:
    payload (Payload): An object containing:
        - numbers (List[float]): A list of numbers to calculate the average.
    token (str): Authentication token for the current user.

Returns:
    dict: A dictionary with:
        - "average" (float): The calculated average of the input numbers.

Raises:
    HTTPException: If the list of numbers is empty or the user is not authenticated.

Example:
    Request payload:
        {
            "numbers": [1, 2, 3, 4, 5]
        }
    Response:
        {
            "average": 3.0
        }
"""
@app.post("/average")
def average(payload: Payload, token: str):
    get_current_user(token)
    numbers = payload.numbers
    if not numbers:
        raise HTTPException(status_code=400, detail="List of numbers cannot be empty")
    return {"average": sum(numbers) / len(numbers)} 

#Blubblesort function
def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n):
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers