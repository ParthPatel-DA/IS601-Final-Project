# Project Name: Final Project (Dosa Restaurant)

IS601 - Web Systems Development - Final Project

## Project Goal:

You will need to create the following endpoints:

| S.No | Method | Path            | Description                                              |
| ---- | ------ | --------------- | -------------------------------------------------------- |
| 1    | POST   | /customers      | creates a customer in the DB given a JSON representation |
| 2    | GET    | /customers/{id} | retrieves a JSON representation of a customer in the DB  |
| 3    | DELETE | /customers/{id} | deletes a customer in the DB                             |
| 4    | PUT    | /customers/{id} | updates a customer in the DB given a JSON representation |
| 5    | POST   | /items          | creates an item in the DB given a JSON representation    |
| 6    | GET    | /items/{id}     | retrieves a JSON representation of an item in the DB     |
| 7    | DELETE | /items/{id}     | deletes an item in the DB                                |
| 8    | PUT    | /items/{id}     | updates an item in the DB given a JSON representation    |
| 9    | POST   | /orders         | creates an order in the DB given a JSON representation   |
| 10   | GET    | /orders/{id}    | retrieves a JSON representation of an order in the DB    |
| 11   | DELETE | /orders/{id}    | deletes an order in the DB                               |
| 12   | PUT    | /orders/{id}    | updates an order in the DB given a JSON representation   |

## Steps to run the project:

```shell
# Windows
pip install -r requirements.txt
py db_init.py
uvicorn main:app --reload

# Mac
pip3 install -r requirements.txt
python3 db_init.py
uvicorn main:app --reload
```

## Result:

To check api result, open below URL in browser:

```shell
http://127.0.0.1:8000/docs
```

## References:

#### Project Requirement:

https://web.njit.edu/~rt494/python_web_api/final-project.html

#### JSON File:

https://raw.githubusercontent.com/rxt1077/IS601/master/midterm_project/example_orders.json
