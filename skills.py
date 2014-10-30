import re
from copy import deepcopy
import requests
import json
from settings import GOOGLE_DOC_URL


def get_skills(path, fetch=True):

    if not fetch:
        with open(path) as f:
            return json.load(f)

    else:
        skills_dl = requests.get(GOOGLE_DOC_URL)
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
        #line = line.encode('ascii', 'replace').rstrip()
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
        """To aid ARM's partners in the design of SoCs and the software to
        run on them, ARM produces software models of our CPUs and
        peripherals so SoCs can be simulated at high speed; this was my area
        of expertise.""",
    },
    {
        "employer": "Imagination Technologies",
        "dates": "2003 to 2005",
        "description":
        """Imagination Technologies designs low-power graphics and video
        processors as well as communications products. I implemented precise
        models of hardware blocks and test harnesses to enable cycle-by-cycle
        validation of hardware designs. The models were also used by
        customers to evaluate the hardware.""",
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
    pprint(get_skills("skills.txt"))