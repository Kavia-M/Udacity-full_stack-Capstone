# The Wedding Event Management
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