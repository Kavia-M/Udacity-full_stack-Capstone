# <img src="https://static.vecteezy.com/system/resources/previews/013/867/280/original/wedding-rings-icon-for-graphic-design-logo-website-social-media-mobile-app-ui-illustration-free-vector.jpg" width=30px> The Wedding Event Management
## Full Stack Web Developer Capstone Project

This is an Application for a Wedding Event Management company. The Database has 2 tables couple and hall. 
The Event Management company has a Manager, Officers and Decorators. The customer is anyone in the Internet who has successfully signed in to the application.

1. The customer can be friends or family members of the couple or the couple themselves who want to avail the service of the wedding event management company. The can post the couple details in the app. Other than this they have none other access. While posting the couple details, the wedding theme and the hall can be left empty since the customer doesn't know the wedding themes offered and the available halls at the time of registering the couple details into the app. The customer will be contacted by the officer through the email ID given. To do any modifications to the couple details like marriage date the customer has to contact the officer.
2. The Officer is the one who interacts with the customers. After the customer posts the couple details, the officer contacts the customer through the email ID provided. They explain about the available halls and the wedding themes offered. And updates the couple data accordingly. The officer has all access to the couple data such as view, create, update and remove. They can also view the halls so that they can explain to the customers
3. The Decorator is the one who decorates the Wedding halls. They can view the halls details so that to know the address and capacity of the hall to be decorated. They have nothing to do with the couple data hence they can't view, edit or delete the couple data. But still decorators are also common people in internet and are authenticated users, they can post a couple details as a customer.
4. The Manager has all the access to the database, both couple and hall table.

This is the final Capstone project of `Udacity - Full Stack Web Developer nanodegree`. All the skills acquired in the nanodegree (listed below) are put together to make this creative project.

- SQL and Data Modeling for the Web
- API Developement and Documentation
- Identity access Management
- Deployment

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

The app is hosted on Render. URL: **https://udacity-full-stack-capstone.onrender.com**

## Getting Started

### Dependencies
- Python
- Pip
- Postman (API testing tool)
- Auth0 authentication
- Key pip dependencies
    - FLask
    - SQLAlchemy
    - Flask-CORS

### Database
The database has 2 tables Couple and Hall
- Fields of Couple Table
    Field name | Explanation | Specification
    --- | --- | --- | 
    `id` | Couple Id  | Integer, Primary Key, autogenerated
    `bride_name` | Name of the bride | String, not null
    `groom_name` |  Name of the groom | String, not null
    `marriage_date` | Date of marriage | Date, not null
    `email_id` | Contact email ID | String, not null
    `wedding_theme` | What kind of wedding |  String, nullable
    `hall` | Id of Hall for wedding | Integer, nullabe, Foreign Key (`id` of `Hall`), When The hall is deleted it is set to null

- Fields of Hall Table
    Field name | Explanation | Specification
    --- | --- | --- | 
    `id` | Hall Id  | Integer, Primary Key, autogenerated, referred by Couple Table
    `name` | Name of the Hall | String, not null
    `capacity` | Number of persons hall can accommodate | Integer, not null
    `price` | Date of marriage | Numeric, maximum 10 digits with 2 decimal digits, not null
    `address` | Address of the hall | String, not null

### Environment variables
Environment variables can be set using terminal with the following command.

```
export key=value
```

Or can be set using `.env` file
- Create `.env` file under root directory. The file is added to .gitignore. So it is not available in github repository
- In the file add the environment variables in the format `key=value` one by one in new line

Note: Don not leave spaces around `=` Do not use `'` or `"` around key or value

The environment variables used here are 
Key | Default value used in code | Explanation
--- | --- | --- |
RESET_DB | Ture | This is used to decide whether to reset the DB while running the app
AUTH0_DOMAIN | udacity-fullstack-kavia-auth.us.auth0.com | The auth0 domain name where the auth application resides
API_AUDIENCE | wedding | The api audience for the auth application
DB_HOST | 127.0.0.1:5432 | Where the DB will be hosted
DB_USER | postgres | Name of the DB User
DB_PASSWORD | postgres | Password for the DB User
DB_NAME  | event_management | Name of production DataBase for the application
DATABASE_URL  | 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME) | URL for the Production DB. It is used in while the application being deployed in Render and DB is hosted in cloud. It is set in the Render application environment variables
TEST_DB_NAME | event_management_test | Test Database used in test.py It is used not to disturb the production database during testing
TEST_DATABASE_URL | 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, TEST_DB_NAME) | Url for the test DB. It is useful if the test db is hosted in cloud
AUTH0_CLIENT_ID | 57b0nWhidtmko1oZidS3mDNiBXoG70aH | Client ID of the auth application in auth0

***Important Environments to be taken care of while running locally***
- RESET_DB (Set this to False while running 2nd time locally)
- DB_USER
- DB_PASSWORD

### Authentication
The Authentication is done using [auth0](https://auth0.com/)

The tokens for different users with different roles can be optained using the curl request. The response will be a JSON with access token.
- Manager
    ```
    curl --request POST \
        --url 'https://udacity-fullstack-kavia-auth.us.auth0.com/oauth/token' \
        --data grant_type=password \
        --data 'client_id=57b0nWhidtmko1oZidS3mDNiBXoG70aH' \
        --data audience=wedding \
        --data username='kavia_testing@testmail.com' \
        --data password='Password1234'

    ```

- Officer
    ```
    curl --request POST \
        --url 'https://udacity-fullstack-kavia-auth.us.auth0.com/oauth/token' \
        --data grant_type=password \
        --data 'client_id=57b0nWhidtmko1oZidS3mDNiBXoG70aH' \
        --data audience=wedding \
        --data username='kavia_testing_officer@testmail.com' \
        --data password='Password*Officer'

    ```

- Decorator
    ```
    curl --request POST \
        --url 'https://udacity-fullstack-kavia-auth.us.auth0.com/oauth/token' \
        --data grant_type=password \
        --data 'client_id=57b0nWhidtmko1oZidS3mDNiBXoG70aH' \
        --data audience=wedding \
        --data username='kavia_testing_decorator@testmail.com' \
        --data password='Password*Decorator'

    ```

- Customer (any one in internet who logged in successfully)
    ```
    curl --request POST \
        --url 'https://udacity-fullstack-kavia-auth.us.auth0.com/oauth/token' \
        --data grant_type=password \
        --data 'client_id=57b0nWhidtmko1oZidS3mDNiBXoG70aH' \
        --data audience=wedding \
        --data username='kavia_testing_customer@testmail.com' \
        --data password='Password*Customer'

    ```

    ***Any one can Sign up as customer and get the token using the [URL](https://udacity-fullstack-kavia-auth.us.auth0.com/authorize?audience=wedding&response_type=token&client_id=57b0nWhidtmko1oZidS3mDNiBXoG70aH&redirect_uri=https://127.0.0.1:8080/login-results). The access token will be a parameter in the redirected url***

### Run locally
Pre-requisitions:
- Python installed
- Pip installed 
- Linux terminal to run commands or Gitbash for windows

Steps:
- Clone this repository
- In terminal (or gitbash), navigate to root directory
- Run the command, `pip install -r requirements.txt`
- **Create 2 databases preferrably with the names `event_management` and `event_management_test` One for the app and the other for testing**
- Set the environment variables espesially RESET_DB to False if needed, DB_USER, DB_PASSWORD, DB_NAME and TEST_DB_NAME
- Run the command, `flask run`
- The IP address will be displayed. The API can be accessed using postman
- Postman collection json provided in the repository can be used or the API can be called sepately with Authorization type as bearer token and using the token got with curl requests mentioned above
- To run test cases in test.py use the command `python test.py` or `python3 test.py` whichever is applicable to the environment of local setup

## API Reference
Please check [here](./api-documentation.md) for detailed API documentation.

## Authors
- Kavia M, an Udacity student from Natwest

## Acknowledgements
Sincere Thanks to,
- Natwest Groups, for providing me an opportunity to take the nanodegree
- Awanish Kumar Sigh, Natwest mentor for the nanodegree
- Udacity Team, for continous support and mentorship
- Vecteezy for [logo](https://www.vecteezy.com/vector-art/13867280-wedding-rings-icon-vector-for-graphic-design-logo-website-social-media-mobile-app-ui-illustration)

### Reference
1. My previous projects as a part of this naodegree
    - [Trivia project file, referred for app.py for end points](https://github.com/Kavia-M/Trivia-files/blob/main/__init__.py)
    - [Coffee Shop app, Identity Access Management Project](https://github.com/Kavia-M/Udacity-Coffee-Shop-project.git)
2. Resources from Udacity Course
    - [The reference code provided in Udacity github repository. This is the code taught in Course lessons. I referred this for auth.py code](https://github.com/udacity/cd0039-Identity-and-Access-Management/blob/master/lesson-2-Identity-and-Authentication/BasicFlaskAuth/app.py)
    - [Udacity course video - referred for check_permissions() function in auth.py This video is in Full Stack Web developer nanodegree -> Course 3 Identity Access Management -> Lesson 4 Access and Authorization -> Concept 4 Using RBAC in Flask](https://www.youtube.com/watch?v=oJTIraxK4UQ&t=1s)
    - [The reference code provided by Udacity in Course 2 API Development and Documentation. Referred for Patch and Delete end points](https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/6_Final_Starter/backend/flaskr/__init__.py)
3. Other sources from internet
    - [Stackoverflow](https://stackoverflow.com/)
    - [Geeks for Geeks](https://www.geeksforgeeks.org/)