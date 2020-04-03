from flask_restful import reqparse, Resource
import sqlite3
import requests

parser = reqparse.RequestParser()

db_path = "./db/jobs.db"


class JobInfo(Resource):
    """
    method to serve data for GET with filter option
    """
    def __init__(self):
        parser.add_argument("location")
        parser.add_argument("title")

    def get(self):
        """
        method to GET JOB LIST
        Filter by : location, title
        """
        args = parser.parse_args()
        print(";;;;;;;;", args)

        # connection utility
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # query generator
        if args.location:
            query = "SELECT * FROM job_profiles WHERE location='{}'".format(args.location)
        elif args.title:
            query = "SELECT * FROM job_profiles WHERE title='{}'".format(args.title)
        else:
            query = "SELECT * FROM job_profiles"

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            data = []

            for i in results:
                data.append(
                    {
                        "id": i[1],
                        "type": i[2],
                        "url": i[3],
                        "created_at": i[4],
                        "company": i[5],
                        "company_url": i[6],
                        "location": i[7],
                        "title": i[8],
                        "description": i[9],
                        "how_to_apply": i[10],
                        "company_logo": i[11],
                    }
                )

            return {
                "status": 200,
                "message": "success",
                "data": data
            }
        except Exception as e:
            return {
                "status": 500,
                "message": "Unexpected Error Occurred",
                "data": []
            }


class FetchJobs(Resource):
    """
    API to trigger fetch method.
    """
    def __init__(self):
        parser.add_argument("location")
        parser.add_argument("description")

    def post(self):
        """
        method to Fetch info from github jobs api and to store in local database.
        args: description, location
        if args given:
            dynamic url will be formed
        else:
            static url will be used
        """

        args = parser.parse_args()

        if args.description or args.location:
            url = "https://jobs.github.com/positions.json?description={0}&location={1}".format(
                args.description,
                args.location.replace(" ", "+"))
        else:
            url = "https://jobs.github.com/positions.json?description=python&location=new+york"

        try:
            req = requests.get(url)  # github job api call 'GET'
            jobs_info = req.json()

            # if status_code is 200 and jobs_info is not null then insert block executed
            # and success response given else no data found response given

            if req.status_code == 200 and jobs_info:
                # connection utility
                connection = sqlite3.connect(db_path)
                cursor = connection.cursor()

                for i in jobs_info:

                    # the query will ignore duplicate records on job_id alias id from api response.
                    # in table the job_id field is set to UNIQUE.

                    query = "INSERT OR IGNORE INTO job_profiles (job_id, type, url, created_at, company, company_url," \
                            "location, title, description, how_to_apply, company_logo) " \
                            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,? ,?)"

                    val = (
                        i["id"],
                        i["type"],
                        i["url"],
                        i["created_at"],
                        i["company"],
                        i["company_url"],
                        i["location"],
                        i["title"],
                        i["description"],
                        i["how_to_apply"],
                        i["company_logo"]
                    )

                    cursor.execute(query, val)  # insert operation
                    connection.commit()

                return {
                    "status": 200,
                    "message": "success"
                }
            else:
                return {
                    "status": 404,
                    "message": "No Data Found for Given args"
                }

        except Exception as e:
            return {
                "status": 500,
                "message": "Unexpected Error Occurred"
            }
