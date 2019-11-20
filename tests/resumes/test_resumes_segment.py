import pytest

from msvdd_bloc.resumes import munge
from msvdd_bloc.resumes import segment


@pytest.fixture(scope="module")
def text():
    return """
John Doe
1234 Fake Street, City Name, XX 12345  |  555-555-5555  |  foo.bar@fake.com

EXPERIENCE
Some Company, \u200bSenior Job Title
New York, NY       Jan 2018 – Mar 2019

● Here is a summary of my responsibilities while I worked at Some Company
● And here are some of my accomplishments from this time, which required great skill and expertise

with a variety of tools that you may find relevant
Another Company, Junior Job Title
San Francisco, CA             Sept 2016 – December 2017

● Look, I even excelled in a junior role at Another Company, by learning how to use
many new tools, which by the way, I see you use too

● Here are some concrete numbers on company KPIs to quantify my value
● Did I mention that I'm a great fit for your role?

EDUCATION
University of Fake Name
B.A. in Computer Science    \u200bSep 2012 - June 2016
Relevant coursework:
● Introduction to Algorithms &amp; Data Structures; Python 101; Machine Learning &amp;
Deep Learning; Intro to Natural Language Processing

SKILLS

● SQL, Mongo, HBase
● Languages: HTML, CSS, JavaScript, Python

● GitHub, Node.js, Flask
● Platforms: AWS, Google Cloud, WordPress
1
"""


@pytest.fixture(scope="module")
def filtered_text_lines(text):
    norm_text = munge.normalize_text(text)
    return munge.get_filtered_text_lines(norm_text)


def test_get_section_lines(filtered_text_lines):
    obs_lines = segment.get_section_lines(filtered_text_lines)
    exp_lines = {
        'education': [
            'University of Fake Name',
            'B.A. in Computer Science    Sep 2012 - June 2016',
            'Relevant coursework:',
            '- Introduction to Algorithms & Data Structures; Python 101; Machine Learning &',
            'Deep Learning; Intro to Natural Language Processing',
            '',
        ],
        'skills': [
            '',
            '- SQL, Mongo, HBase',
            '- Languages: HTML, CSS, JavaScript, Python',
            '- GitHub, Node.js, Flask',
            '- Platforms: AWS, Google Cloud, WordPress',
        ],
        'start': [
            'John Doe',
            '1234 Fake Street, City Name, XX 12345  |  555-555-5555  |  foo.bar@fake.com',
            '',
        ],
        'work': [
            'Some Company, Senior Job Title',
            'New York, NY    Jan 2018 – Mar 2019',
            '',
            '- Here is a summary of my responsibilities while I worked at Some Company',
            '- And here are some of my accomplishments from this time, which required great skill and expertise',
            '',
            'with a variety of tools that you may find relevant',
            'Another Company, Junior Job Title',
            'San Francisco, CA    Sept 2016 – December 2017',
            '',
            '- Look, I even excelled in a junior role at Another Company, by learning how to use',
            'many new tools, which by the way, I see you use too',
            '',
            '- Here are some concrete numbers on company KPIs to quantify my value',
            "- Did I mention that I'm a great fit for your role?",
            '',
        ]
    }
    assert sorted(obs_lines.keys()) == sorted(exp_lines.keys())
    for key in exp_lines.keys():
        assert obs_lines[key] == exp_lines[key]
