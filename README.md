
.pylintrc has been created with following command
pylint --generate-rcfile > .pylintrc

pytest.ini is a configuration file for pytest having higest configuration precedence. -s argument says python print() function 
prints to the console.


To Start applicationuse the following command
template>uvicorn pydrapp.main:app --port 8003 --log-config log4py.yaml --reload --reload-dir pydrapp

### Knowledge of Code & Progress
Repository patient-service-system, now onwards(3rd Dec 21), is considered a monolith  python code base. It has been set monolith satus to reduce complexity of microservice deployment. Python with FastAPI has been used for writing Rest API. Along with patien-serivce dao layer(Microservice), every module, every aspect, anyting could be write here and client app/UI can integrte exposed API. Keep in mind, write anything here with microservice perespective and able to deploy independently.

## pytest-user-service
pytest-user-service is considered as integration test pack to test all the API in patient-service-system monolith. Currently(4th Dec 2021) integration test are written for following microservices.

Markup: 1. patient-service-system
        2. medicine-service-system (only create)
        3. catch