from datetime import timedelta, datetime
from fastapi import FastAPI, Path, Query, Depends, HTTPException
from src.models import Employee, NewEmployee, User, NewUser
import json
from mongoengine import connect
from mongoengine.queryset.visitor import Q
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from .config import pwd_context, oauth2_scheme, SECRET_KEY, ALGORITHM


app = FastAPI(title="study project", description="API by Aexandra Vorobeva")
connect(db="hrms", host='localhost', port=27017)


@app.get('/get_all_employees')
def get_all_employees():
    employees = json.loads(Employee.objects().to_json())
    return {"employees": employees}


@app.get('/get_employee/{emp_id}')
def get_employee(emp_id: int = Path(...,gt=0)):
    employee = Employee.objects.get(emp_id=emp_id)
    employee_dict = {
        "emp_id": employee.emp_id,
        "name": employee.name,
        "age": employee.age,
        "teams":employee.team,
    }
    return employee_dict


@app.get("/search_employees")
def search_employees(name: str, age: int = Query(None, gt=18)):
    employees = json.loads(Employee.objects.filter(Q(name__icontains=name) | Q(age=age)).to_json())
    return {"employees": employees}


@app.post("/add_employee")
def add_employee(employee: NewEmployee):
    new_employee = Employee(emp_id=employee.emp_id,
                            name=employee.name,
                            age=employee.age,
                            team=employee.team
                            )
    new_employee.save()
    return {"message": "Employee added successfully"}


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/sign_up")
def sign_up(new_user: NewUser):
    user = User(username=new_user.username,
                password=get_password_hash(new_user.password))
    user.save()
    return {"message": "New user created successfully"}


def authenticate_user(username, password):
    try:
        user = json.loads(User.objects.get(username=username).to_json())
        password_check = pwd_context.verify(password, user["password"])
        return password_check
    except User.DoesNotExist:
        return False


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if authenticate_user(username, password):
        access_token = create_access_token(data={"sub": username}, expires_delta=timedelta(minutes=30))
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")


@app.get('/')
def home(token: str = Depends(oauth2_scheme)):
    return {"token": token}






