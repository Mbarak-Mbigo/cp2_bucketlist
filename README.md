[![Build Status](https://travis-ci.org/Mbarak-Mbigo/cp2_bucketlist.svg?branch=develop)](https://travis-ci.org/Mbarak-Mbigo/cp2_bucketlist)
[![Coverage Status](https://coveralls.io/repos/github/Mbarak-Mbigo/cp2_bucketlist/badge.svg?branch=develop)](https://coveralls.io/github/Mbarak-Mbigo/cp2_bucketlist?branch=develop) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
# cp2_bucketlist
## Bucket List Application
Is a token based rest API (Application Programming Interface) created using python3, flask and flask restful.
You can create bucketlists, bucketlist items operate on them through the API endpoints.

## How to Run this service locally
clone the repository:
> https://github.com/Mbarak-Mbigo/cp2_bucketlist.git

### Create a Virtual environment:
You can use this [guide!](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/)

### Activate virtual environment and

#### Install requirements
> pip -r install requirements.txt

### Run database related commands:

#### create and drop tables
> ./manage.py create_db  
> ./manage.py drop_db

#### create migrations directory
> ./manage.py db init

#### migrate
> ./manage.py db migrate

#### apply migrations
> ./manage.py db upgrade

### Run server:
> ./manage.py runserver

### Access server:
> http://127.0.0.1:5000/

## How to consume the API
BucketList API exposes a number of endpoints some are public and 
some are private (You have to register and login to access them)

## Public endpoints:
Public Endpoints |  Purpose
------------------|------------
POST /auth/register | user registration
POST /auth/login | user login

## Protected/Private endpoints

### Note: for the current version append **`api/v1/`**
e.g. http://127.0.0.1:5000/api/v1/bucketlists/

Private Endpoints | Purpose
----------| -------------
POST /bucketlists/ | Create a new bucket list
GET /bucketlists/ | List all the created bucket lists
GET /bucketlists/<id> | Get single bucket list
PUT /bucketlists/<id> | Update this bucket list
DELETE /bucketlists/<id> | Delete this single bucket list
POST /bucketlists/<id>/items/| Create a new item in bucket list
PUT /bucketlists/<id>/items/<item_id> | Update a bucket list item
DELETE /bucketlists/<id>/items/<item_id> | Delete an item in a bucket list

#### searching urls are built with a **`?q=`**
  e.g http://127.0.0.1:5000/api/v1/bucketlists/?q=swim

#### Default paginated queries are 20 items per page
> example: http://127.0.0.1:5000/api/v1/bucketlists/?limit=20&page=2

You can adjust the number of buckets per page by specfying the `limit` query with a number
> http://127.0.0.1:5000/api/v1/bucketlists/?limit=3

Note: Maximum results per page is **`100`**








