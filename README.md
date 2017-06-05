[![Build Status](https://travis-ci.org/jimmykimani/Bucketlist.svg?branch=master)](https://travis-ci.org/jimmykimani/Bucketlist) [![Jimmy Kimani](https://img.shields.io/badge/Jmmy%20Kimani-Checkpoint2-green.svg)]()

# What is a Bucketlist?

Simply it is a list of all the goals you want to achieve, dreams you want to fulfill and life experiences you desire to experience before you die.

# Bucketlist API

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

# INSTALLATION & SET UP.

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
