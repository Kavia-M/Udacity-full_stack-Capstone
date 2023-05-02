# API Documentation
The Database of the Wedding Event Management application has two Tables namely `couple` and `hall`. 

## Getting started
- Base URL: **https://udacity-full-stack-capstone.onrender.com** For Local deployment use `http://127.0.0.1:5000`

## Errors
Errors are returned as JSON objects in the following format:
```json
{
    "success" : false,
    "error": 404,
    "message": "resource not found"
}
```
The possible errors are:

Error code | Error type |
--- | --- |
400 | Bad request
400 | Invalid claims - Permissions not included in JWT
401 | Unauthorized
403 | Forbidden - Permission not found
404 | Resource Not Found
405 | Method not allowed
422 | Unprocessable
500 | Internal Server Error

In the above errors, 400 invalid claims and 401 unauthorized can happen at any endpoint if the header or JWT is misformatted.

403 can happen is the user is authenticated but not have enough permissions to that endpoint. Accessible endpoints for each role are listed below.

## Roles
- Anyone on the internet successfullly signed up (authenticated) and has a valid JWT (no permissions required)
  - POST /couples
- Decorator
  - POST /couples
  - GET /halls
  - GET /halls/<hall_id>
- Officer
  - GET /couples
  - GET /couples/<couple_id>
  - POST /couples
  - PATCH /couples/<couple_id>
  - DELETE /couples/<couple_id>
  - GET /halls
  - GET /halls/<hall_id>
- Manager
  - GET /couples
  - GET /couples/<couple_id>
  - POST /couples
  - PATCH /couples/<couple_id>
  - DELETE /couples/<couple_id>
  - GET /halls
  - GET /halls/<hall_id>
  - POST /halls
  - PATCH /halls/<hall_id>
  - DELETE /halls/<hall_id>

## Endpoints

### `GET '/'`
- General:
    - Health checkup endpoint.
    - Always returns a string `"Healthy"`
    - No authentication authorization required
- **Possible errors** : 
    - ***No Errors Possible*** Always 200 success

- Sample request in Postman
  - URL:  `GET <BASE_URL>/`
  - Response:
```
Healthy
```
### `GET '/couples'`

- General:
    - To get the list of all couples as an array with the details such as `id`, `bride_name`, `groom_name`, `marriage_date`, `email_id`, `wedding_theme` and `hall` where `hall` is the hall id and is a foreign key
    - It also returns `total_cpuples` which is length of the array and `success` which is a boolean value
- **Possible errors** : 
    - ***404*** if no couple exists in the database

- Sample request in Postman
  - URL:  `GET <BASE_URL>/couples`
  - Response:
```json
{
    "couples": [
        {
            "bride_name": "Bride",
            "email_id": "abc@gmail.com",
            "groom_name": "groom",
            "hall": 1,
            "id": 1,
            "marriage_date": "Mon, 28 Mar 2022 04:00:55 GMT",
            "wedding_theme": "Indian Grand look"
        },
        {
            "bride_name": "Bride1",
            "email_id": "abcdef@gmail.com",
            "groom_name": "groom1",
            "hall": "Yet to be decided",
            "id": 2,
            "marriage_date": "Sat, 20 May 2023 03:30:00 GMT",
            "wedding_theme": "Yet to be decided"
        },
        {
            "bride_name": "Bride2",
            "email_id": "abcdefghijkl@gmail.com",
            "groom_name": "groom2",
            "hall": "Yet to be decided",
            "id": 3,
            "marriage_date": "Tue, 20 Jun 2023 03:00:00 GMT",
            "wedding_theme": "Yet to be decided"
        }
    ],
    "success": true,
    "total_couples": 3
}
```
### `GET '/couples/<couple_id>'`
- General:
    - Fetches the couple with the couple id provided
    - Request Path Arguments: `couple_id` - integer which is couple id
    - Returns: the couple details such as `id`, `bride_name`, `groom_name`, `marriage_date`, `email_id`, `wedding_theme` and `hall` where `hall` is the hall id and is a foreign key
    - It also returns `success` which is a boolean value
- **Possible errors** : 
    - ***404*** if no couple is found with the given id
- Sample request in Postman
  - URL:  `GET <BASE_URL>/couples/2`
  - Response:
```json
{
    "couple": {
        "bride_name": "Bride1",
        "email_id": "abcdef@gmail.com",
        "groom_name": "groom1",
        "hall": "Yet to be decided",
        "id": 2,
        "marriage_date": "Sat, 20 May 2023 03:30:00 GMT",
        "wedding_theme": "Yet to be decided"
    },
    "success": true
}
```

### `POST '/couples'`
- General:
    - Sends a post request in order to create a new couple in the database
    - It expexts Request Body  with the details such as `bride_name`, `groom_name`, `marriage_date`, `email_id`, `wedding_theme` and `hall` of the couple with the fields in correct format where `hall` is the hall id and is a foreign key **Marriage_date should be in format YYYY-MM-DD HH:MM:SS** marriage_theme and hall fields are optional
    - It inserts the new question to the database and returns `success` boolean value, `created` which is the newly created couple details
- **Possible errors** : 
    - ***422*** if foreign key violation that is hall id provided is actually not present in hall table
    - ***400*** if Date Error that marriage date provided is not in correct format or invalid date
    - ***422*** if some other error occurs during insertion into the database

- Sample request in Postman
  - URL:  `POST <BASE_URL>/couples`
  - Request Body of type Raw JSON: 
```json
{
    "bride_name" : "new_bride_officer",
    "groom_name" : "new_groom_officer",
    "marriage_date" : "2023-07-28 5:00:55",
    "email_id" : "new_officer@gmail.com",
    "hall" : 2
}
  ```
- Response: 
```json
{
    "created": {
        "bride_name": "new_bride_officer",
        "email_id": "new_officer@gmail.com",
        "groom_name": "new_groom_officer",
        "hall": 2,
        "id": 4,
        "marriage_date": "Fri, 28 Jul 2023 05:00:55 GMT",
        "wedding_theme": "Yet to be decided"
    },
    "success": true
}  
```

### `PATCH '/couples/<couple_id>'`
- General:
    - Updates the couple with the couple id by the details provided
    - It expexts Request Body with the details such as `bride_name`, `groom_name`, `marriage_date`, `email_id`, `wedding_theme` and `hall` of the couple with the fields in correct format where `hall` is the hall id and is a foreign key **Marriage_date should be in format YYYY-MM-DD HH:MM:SS** not all fields are mandatory 
    - It inserts the new question to the database and returns `success` boolean value, `updated` which is the newly updated couple details
- **Possible errors** : 
    - ***404*** if couple id in the url does not exists
    - ***422*** if foreign key violation that is hall id provided is actually not present in hall table
    - ***400*** if Date Error that marriage date provided is not in correct format or invalid date
    - ***422*** if some other error occurs during update into the database

- Sample request in Postman
  - URL:  `PATCH <BASE_URL>/couples/2`
  - Request Body of type Raw JSON: 
```json
{
    "marriage_date" : "2023-06-28 4:00:00",
    "email_id" : "updated_email@gmail.com",
    "wedding_theme" : "Grand Tamil Traditional",
    "hall" : 2
}
  ```
- Response: 
```json
{
    "success": true,
    "updated": {
        "bride_name": "Bride1",
        "email_id": "updated_email@gmail.com",
        "groom_name": "groom1",
        "hall": 2,
        "id": 2,
        "marriage_date": "Wed, 28 Jun 2023 04:00:00 GMT",
        "wedding_theme": "Grand Tamil Traditional"
    }
} 
```

### `DELETE '/couples/<couple_id>'`
- General:
    - Deletes a specified couple using the couple id given
    - Request Path Arguments: `couple_id` - integer which is couple id
    - Returns the `success` boolean value, `deleted` which is the id of the deleted couple, `total_couples` which is number of couples in the database after deletion and `couples` which is list of all couples in the database after deletion with the details such as `id`, `bride_name`, `groom_name`, `marriage_date`, `email_id`, `wedding_theme` and `hall` of the couples with the fields in correct format where `hall` is the hall id and is a foreign key
- **Possible errors** : 
    - ***404*** if couple id in the url does not exists
    - ***422*** if some error during deletion from the database
- Sample request in Postman
  - URL:  `DELETE <BASE_URL>/couples/1`
- Response: 
```json
{
    "couples": [
        {
            "bride_name": "Bride1",
            "email_id": "updated_email@gmail.com",
            "groom_name": "groom1",
            "hall": 2,
            "id": 2,
            "marriage_date": "Wed, 28 Jun 2023 04:00:00 GMT",
            "wedding_theme": "Grand Tamil Traditional"
        },
        {
            "bride_name": "Bride2",
            "email_id": "abcdefghijkl@gmail.com",
            "groom_name": "groom2",
            "hall": "Yet to be decided",
            "id": 3,
            "marriage_date": "Tue, 20 Jun 2023 03:00:00 GMT",
            "wedding_theme": "Yet to be decided"
        },
        {
            "bride_name": "new_bride_officer",
            "email_id": "new_officer@gmail.com",
            "groom_name": "new_groom_officer",
            "hall": 2,
            "id": 4,
            "marriage_date": "Fri, 28 Jul 2023 05:00:55 GMT",
            "wedding_theme": "Yet to be decided"
        }
    ],
    "deleted": 1,
    "success": true,
    "total_couples": 3
}
```

### `GET '/halls'`
- General:
    - To get the list of all halls as an array with the details such as `id`, `name`, `capacity (number of persons)`, `price (per day)`, `address`
    - It also returns `total_halls` which is length of the array and `success` which is a boolean value
- **Possible errors** : 
    - ***404*** if no hall exists in the database

- Sample request in Postman
  - URL:  `GET <BASE_URL>/halls`
  - Response:
```json
{
    "halls": [
        {
            "address": "20, Kuppander Street-1, Pudhupalayam, Gobichettipalayam",
            "capacity (number of persons)": 500,
            "id": 1,
            "name": "Raj Mahal",
            "price (per day)": "60000.00"
        },
        {
            "address": "Erode, Tamil Nadu",
            "capacity (number of persons)": 400,
            "id": 2,
            "name": "Seetha Kalyana Mandapam",
            "price (per day)": "20000.00"
        }
    ],
    "success": true,
    "total_halls": 2
}
```
### `GET '/halls/<hall_id>'`
- General:
    - Fetches the hall with the hall id provided
    - Request Path Arguments: `hall_id` - integer which is hall id
    - Returns: the hall details such as with the details such as `id`, `name`, `capacity (number of persons)`, `price (per day)`, `address`
    - It also returns `success` which is a boolean value
- **Possible errors** : 
    - ***404*** if no hall is found with the given id
- Sample request in Postman
  - URL:  `GET <BASE_URL>/halls/2`
  - Response:
```json
{
    "hall": {
        "address": "Erode, Tamil Nadu",
        "capacity (number of persons)": 400,
        "id": 2,
        "name": "Seetha Kalyana Mandapam",
        "price (per day)": "20000.00"
    },
    "success": true
}
```

### `POST '/halls'`
- General:
    - Sends a post request in order to create a new hall in the database
    - It expexts Request Body with the details such as `name`, `capacity`, `price`, `address` where capacity is the number of the capacity is the number of persons the hall can accomoddate and price is the amount in rupees (2 decimal digits are optional). Capacity and price are numbers and others are strings
    - It inserts the new question to the database and returns `success` boolean value, `created` which is the newly created hall details
- **Possible errors** : 
    - ***422*** if a mandatory field is missing in the request body
    - ***422*** if the datatype doesn't match for any of the field
    - ***422*** if some other error occurs during insertion into the database

- Sample request in Postman
  - URL:  `POST <BASE_URL>/halls`
  - Request Body of type Raw JSON: 
```json
{
    "name": "Mahindra",
    "capacity": 500,
    "price": 30000,
    "address": "Tamil Nadu, Chennai"            
}
  ```
- Response: 
```json
{
    "created": {
        "address": "Tamil Nadu, Chennai",
        "capacity (number of persons)": 500,
        "id": 3,
        "name": "Mahindra",
        "price (per day)": "30000.00"
    },
    "success": true
}  
```

### `PATCH '/halls/<hall_id>'`
- General:
    - Updates the hall with the hall id by the details provided
    - It expexts Request Body with the details such as `name`, `capacity`, `price`, `address` where capacity is the number of the capacity is the number of persons the hall can accomoddate and price is the amount in rupees (2 decimal digits are optional). Capacity and price are numbers and others are strings. Not all fields are mandatory 
    - It inserts the new question to the database and returns `success` boolean value, `updated` which is the newly updated hall details
- **Possible errors** : 
    - ***404*** if hall id in the url does not exists
    - ***422*** if the datatype doesn't match for any of the field
    - ***422*** if some other error occurs during update into the database

- Sample request in Postman
  - URL:  `PATCH <BASE_URL>/halls/2`
  - Request Body of type Raw JSON: 
```json
{
    "capacity": 100,
    "price": 100000
}
  ```
- Response: 
```json
{
    "success": true,
    "updated": {
        "address": "Erode, Tamil Nadu",
        "capacity (number of persons)": 100,
        "id": 2,
        "name": "Seetha Kalyana Mandapam",
        "price (per day)": "100000.00"
    }
}
```

### `DELETE '/halls/<hall_id>'`
- General:
    - Deletes a specified hall using the hall id given
    - Request Path Arguments: `hall_id` - integer which is hall id
    - Returns the `success` boolean value, `deleted` which is the id of the deleted hall, `total_halls` which is number of halls in the database after deletion and `halls` which is list of all halls in the database after deletion with the details such as `id`, `name`, `capacity (number of persons)`, `price (per day)`, `address`
- **Possible errors** : 
    - ***404*** if hall id in the url does not exists
    - ***422*** if some error during deletion from the database
- Sample request in Postman
  - URL:  `DELETE <BASE_URL>/halls/1`
- Response: 
```json
{
    "deleted": 1,
    "halls": [
        {
            "address": "Erode, Tamil Nadu",
            "capacity (number of persons)": 100,
            "id": 2,
            "name": "Seetha Kalyana Mandapam",
            "price (per day)": "100000.00"
        },
        {
            "address": "Tamil Nadu, Chennai",
            "capacity (number of persons)": 500,
            "id": 3,
            "name": "Mahindra",
            "price (per day)": "30000.00"
        }
    ],
    "success": true,
    "total_halls": 2
}
```
    