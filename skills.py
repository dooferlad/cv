import re
from copy import deepcopy
import requests
import json
import os
from settings import SKILLS_URL, JOBS_URL, EDUCATION_URL


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
    path = os.path.join(BASE_DIR, "jobs.json")
    return get_list(path, EDUCATION_URL, fetch)

def get_list(path, url, fetch, translate_names={}):
    if not fetch:
        with open(path) as f:
            return json.load(f)

    else:
        skills_dl = requests.get(url)
        skills_dl.encoding = "utf-8-sig"
        skills_text = skills_dl.text

    data = []
    name = None

    for line in skills_text.splitlines():
        line = line.rstrip()
        bits = re.split('\*\s+', line)
        if len(line) and len(bits) == 2:
            if bits[0] == '':
                name = bits[1].lower()
                if name == 'name':
                    data.append({})
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
    with open(path, "w") as f:
        json.dump(data, f)

    return data

career = [
    {
        "employer": "ARM/Linaro",
        "dates": "2011 to 2014",
        "description":
        """As a member of the Linaro Infrastructure team I maintained our
        continuous integration services and developed tools and web
        applications to aid other software engineers as they improve
        Linux on ARM.""",
    },
    {
        "employer": "ARM",
        "dates": "2005 to 2011",
        "description":
        """I implemented models of ARM hardware to aid ARM's partners in the
        design of SoCs and writing the software to run on them.""",
    },
    {
        "employer": "Imagination Technologies",
        "dates": "2003 to 2005",
        "description":
        """I implemented precise
        models of video processing hardware to enable cycle-by-cycle
        validation of hardware designs, and to demonstrate planned functionality
        to customers.""",
    },
    {
        "employer": "AMCC",
        "dates": "2001 to 2003",
        "description":
        """AMCC designs hardware for high-speed networking equipment. I
        created software models of networking parts to use as a reference
        for hardware validation and to research algorithms to shape network
        traffic.""",
    },
]

education = [
    {
        "institution": "University of Manchester Institute of Science & Technology",
        "qualifications": ["Microelectronic Systems Engineering: MEng (Hons), 2.1 class"],
        "dates": "1997 to 2001",
    },
    {
        "institution": "Hull College",
        "qualifications": [
            "A Level Mathematics (B)",
            "BTEC ND Electronics & Communications (Pass)"
        ],
        "dates": "1995 to 1997",
    },
    {
        "institution": "Wolfreton School",
        "qualifications": ["9 GCSEs"],
        "dates": "1990 to 1995"
    },
]

if __name__ == '__main__':
    from pprint import pprint
    from settings import JOBS_URL, SKILLS_URL
    pprint(get_jobs("jobs.json", JOBS_URL, True))
