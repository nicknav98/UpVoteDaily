
# Upvote! Full Stack Python CRUD application

This project aims to deploy a service similar to reddit where users can submit posts that they find interesting for the day - posts that recieve the most upvotes are periodically shown, with the submissions being wiped every 24 hours. 

The aim is deploy the front end using Vue.js as the DOM manipulator, with vanilla javascript to facilitate transactions between front-end forms and the backend. 

The backend API is written in Python using FastAPI as the framework, and SQLAlchemey as the ORM Manager - the upside is that FastAPI relies on Pydantic for data validation.

Check out FastAPI documentation here: https://fastapi.tiangolo.com

The stack includes: Vue.JS Front End, Uvicorn Backend, API built in Python, and PostgreSQL. 




## Deployment

To deploy, install either Docker or PostgreSQL on your local machine.

If you want to use the Docker-Compose File, simply run: 

```bash
  docker-compose up -d 
```

This will run a PostgreSQL container on your local network. 

It's recommended to have a virtualenv, so that the requirements are handled seperately, run

```bash
  pip install -r requirements.txt 
```

and then: 

```bash
  uvicorn main:app 
```

This will run the API on port 8000. 

Further steps will be added once development procceeds 
## API Reference


### TO BE EDITED ONCE API URL's and Tested and Functional
#### Get all items

```http
  GET /api/items
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

#### Get item

```http
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.

