from flask import Flask
from flask_restful import Api
from api.jobs import JobInfo, FetchJobs

app = Flask(__name__)
api = Api(app)

api.add_resource(JobInfo, "/jobs", endpoint="job-info")
api.add_resource(FetchJobs, "/jobs/sync", endpoint="fetch-jobs")


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
