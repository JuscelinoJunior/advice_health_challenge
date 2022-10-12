# advice_health_challenge

### To run locally

Run the command: `docker-compose up -d`

The app address: http://0.0.0.0:5050
The API address: http://0.0.0.0:8080

API Documentation: http://0.0.0.0:5050/api_documentation.html

### Technologies
- OpenAPI (to define the routes and rules for the API)
- Python
- Pytest
- Connexion
- Flask
- SQAlchemy
- MySQL
- HTML + CSS + JS (Frontend)

### The App

The system has some operations: Add a car/owner or delete a car/owner. An owner can't be deleted if he still has a car, and a owner can have only three
cars.

A look:
![image](https://user-images.githubusercontent.com/23690136/195309100-c10620f4-fe59-4fb7-9c79-e553dc60ed8c.png)
![image](https://user-images.githubusercontent.com/23690136/195309231-8bbd96d8-dc52-4b97-be6b-400a0f64da86.png)
![image](https://user-images.githubusercontent.com/23690136/195309403-c23e82f5-ed68-41a9-86e3-916ac6c7f585.png)
