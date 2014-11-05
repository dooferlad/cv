import re
from copy import deepcopy
import requests
import json
import os
from settings import SKILLS_URL, JOBS_URL, EDUCATION_URL, CAREER_URL


BASE_DIR = os.path.dirname(__file__)


def get_skills(fetch=True):
    path = os.path.join(BASE_DIR, "skills.json")
    if not fetch:
        with open(path) as f:
            return json.load(f)

    else:
        skills_dl = requests.get(SKILLS_URL)
        skills_dl.encoding = "utf-8-sig"
        skills_text = skills_dl.text

    state = "name"

    skills = []
    skill_template = {
        "names": [],
        "examples": [],
    }
    skill = deepcopy(skill_template)

    for line in skills_text.splitlines():
        line = line.rstrip()
        bits = re.split('\*\s+', line)
        if len(line) and len(bits) == 2:
            if bits[0] == '':
                if state != "name":
                    skills.append(skill)
                    skill = deepcopy(skill_template)

                skill["names"].append(bits[1])
                state = "name"
            elif len(bits[0]) == 3:
                skill["examples"].append(bits[1])
                state = "example"

    if skill["names"] and skill["examples"]:
        skills.append(skill)

    with open(path, "w") as f:
        json.dump(skills, f)

    return skills

def get_jobs(fetch=True):
    path = os.path.join(BASE_DIR, "jobs.json")
    translate_names = {
        "required skills & experience": "spec",
        "desired skills & experience": "spec",
    }

    return get_list(path, JOBS_URL, fetch, translate_names)

def get_education(fetch=True):
    path = os.path.join(BASE_DIR, "education.json")
    return get_list(path, EDUCATION_URL, fetch)


def get_career(fetch=True):
    path = os.path.join(BASE_DIR, "career.json")
    return get_list(path, CAREER_URL, fetch)


def get_list(path, url, fetch, translate_names={}):
    if not fetch:
        with open(path) as f:
            return json.load(f)

    else:
        skills_dl = requests.get(url)
        skills_dl.encoding = "utf-8-sig"
        skills_text = skills_dl.text

    data = [{}]
    name = None

    for line in skills_text.splitlines():
        line = line.rstrip()
        bits = re.split('\*\s+', line)
        if len(line) and len(bits) == 2:
            if bits[0] == '':
                name = bits[1].lower()
                if name in translate_names:
                    name = translate_names[name]
                if not data[-1].get(name):
                    data[-1][name] = None
            elif len(bits[0]) == 3:
                if data[-1][name] is None:
                    data[-1][name] = bits[1]
                elif not isinstance(data[-1][name], list):
                    temp = [data[-1][name], bits[1]]
                    data[-1][name] = temp
                else:
                    data[-1][name].append(bits[1])
        elif len(line) == 0 and (len(data) == 0 or len(data[-1].keys())):
            data.append({})

    with open(path, "w") as f:
        json.dump(data, f)

    return data


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_career())
