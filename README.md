[![Build Status](https://travis-ci.org/jimmykimani/Bucketlist.svg?branch=master)](https://travis-ci.org/jimmykimani/Bucketlist)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac0ea7159b464c4e97f06eab027ea69b)](https://www.codacy.com/app/jimmykimani/Bucketlist?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jimmykimani/Bucketlist&amp;utm_campaign=Badge_Grade)
[![Jimmy Kimani](https://img.shields.io/badge/Jmmy%20Kimani-Checkpoint2-green.svg)]()

## What is a Bucketlist?

Simply it is a list of all the goals you want to achieve, dreams you want to fulfill and life experiences you desire to experience before you die.

## Bucketlist API

A flask based API to avail resources for creation of bucketlists
>[Flask](http://flask.pocoo.org/) is a common microframework for the Python programming language.

# SCOPE

|Method | Endpoint | Usage |
| ---- | ---- | --------------- |
|POST| `/api/v1/auth/register` |  Register a user. |
|POST| `/api/v1/auth/login` | Login user.|
|POST| `/api/v1/bucketlists/` | Create a new bucket list. |
|GET| `/api/v1/bucketlists/` | Retrieve all the created bucket lists. |
|GET| `/api/v1/bucketlists/<bucket_id>` | Get a single bucket list. |
|PUT| `/api/v1/bucketlists/<bucket_id>` | Update a single bucket list. |
|DELETE| `/api/v1/bucketlists/<bucket_id>` | Delete single bucket list. |
|POST| `/api/v1/bucketlists/<bucket_id>/items` | Add a new item to this bucket list. |
|PUT|`/api/v1/bucketlists/<bucket_id>/items/<item_id>` | Update this bucket list. |
|DELETE|`/api/v1/bucketlists/<bucket_id>/items/<item_id>` | Delete this single bucket list. |
|GET| `/api/v1/bucketlists?per_page=10&page=1` | Pagination to get 10 bucket list records.|
|GET| `/api/v1/bucketlists?q=a bucket` | Search for bucket lists with name like a bucket. 

## INSTALLATION & SET UP.

1. Clone the project on github: 

2. Checkout into the develop branch using ```git checkout develop```

3. Create a ***virtual environment*** and start the virtual environment

4. Install the dependencies via ```pip install -r requirements.txt```

**Setup Database:**

Install postgres and create database bucket_list

**Run the Migrations**:
1. ```python manage.py db init```

2. ```python manage.py db migrate```

3. ```python manage.py db upgrade```

> The server should be running on [http://127.0.0.1:5000] 

## HOW TO USE

First install postman from here

Copy the link `http://127.0.0.1:5000/` and append **api/v1.0/auth/register** 

- **Register a user.**

    ![register](https://i.imgur.com/QIspUlt.png)
    ```
        [POST] http://127.0.0.1:5000/api/v1/auth/register/
    ```
    ```{"username":"jimmykimani", "password":"python"}```

- **Login a user.**

- Change to **api/v1.0/auth/login** but the link remain the same

    ![login](https://i.imgur.com/AHrWyxd.png)
    ```
        [POST] http://127.0.0.1:5000/api/v1/auth/register/
    ```
    ```{"username":"jimmykimani", "password":"python"}```

- Copy only the token as shown below to the headers

    ![token](https://i.imgur.com/xcc5wnn.png)

- **Create a bucketlist**

    To create a bucketlist, make a **POST** request to the following URI:
    **http://127.0.0.1:5000/api/v1/bucketlists/**.

    ![login](https://i.imgur.com/mlsoxAq.png)

    ```
        [POST] http://127.0.0.1:5000/api/v1/bucketlists/
    ```    
    ```{"name":,"My new bucketlist"}```