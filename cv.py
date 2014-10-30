from flask import (
    Flask,
    send_file,
)

import os
import json
from skills import get_skills, career, education
from jobs import jobs

BASE_DIR = os.path.dirname(__file__)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return send_file(os.path.join(BASE_DIR, "static/index.html"))


@app.route('/API/skills')
def api_skills():
    return json.dumps(get_skills(os.path.join(BASE_DIR, "skills.txt"), False))

@app.route('/API/career')
def api_career():
    return json.dumps(career)

@app.route('/API/education')
def api_education():
    return json.dumps(education)

@app.route('/API/jobs')
def api_jobs():
    return json.dumps(jobs)

if __name__ == '__main__':
    app.debug = True
    app.run()
