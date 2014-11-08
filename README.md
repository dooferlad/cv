# cv
Flask and AngularJS generate a CV based on a job spec.

## Why?
Because sometimes you just need to turn a task into a programming problem.

## OK, how?
This takes a Google doc, exports it as text and interprets any unordered lists as a list of skills and examples of those
skills. Top level items are skills and first level indents are examples. You can have multiple skill names for the same
list of examples.

To generate the CV the AngularJS app requests a list of job specs from the server and matches a found job ID to the one
listed in the URL. It then takes the list of skills that the job requests (another Google doc) and matches them to
skills I have listed that I have. Those are inserted into the document using AngularJS's template system. My list of 
qualifications and job history are also fetched from the server and rendered (yet more Google docs).

The source Google docs are listed in settings.py, which you need to create in the form:

```python
BASE_URL = 'https://docs.google.com/feeds/download/documents/export/Export?exportFormat=txt&id='

SKILLS_URL = BASE_URL + '<id of skills doc>'
JOBS_URL = BASE_URL + '<id of jobs doc>'
EDUCATION_URL = BASE_URL + '<id of education doc>'
CAREER_URL = BASE_URL + '<id of career doc>'
```

The layout for the document uses Bootstrap CSS with some custom style rules in media.css. The layout should look good
on devices of all sizes. When printing the body text is rendered in a font with serifs because this tends to be easier
to read on paper, while sans-serif fonts are often better on low DPI screens.