# job-api

job-api is a Python REST API. 
The API fetchs data from `github jobs` API and stores in sqlite. 
It Provides methods to trigger fetch operation and to serve job data.

- to trigger fetch operation
  `POST /jobs/sync`
- to GET data
  `GET /jobs`

###### dependencies

```
flask
flask-restful
requests
```

###### To Run the Project

- create a virtual environment
- install dependencies using the `requirements.txt`
- activate virtual environment
- run `python app.py`
