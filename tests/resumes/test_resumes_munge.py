import pytest

import msvdd_bloc


EXAMPLE_TEXT = """
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
● Introduction to Algorithms and Data Structures; Python 101; Machine Learning and
Deep Learning; Intro to Natural Language Processing

SKILLS

● SQL, Mongo, HBase
● Languages: HTML, CSS, JavaScript, Python

● GitHub, Node.js, Flask
● Platforms: AWS, Google Cloud, WordPress
1
"""

def test_normalize_text():
    norm_text = msvdd_bloc.resumes.munge.normalize_text(EXAMPLE_TEXT)
    assert isinstance(norm_text, str)
    assert not any(char in norm_text for char in ("\u200b", "●"))


def test_get_filtered_text_lines():
    norm_text = msvdd_bloc.resumes.munge.normalize_text(EXAMPLE_TEXT)
    lines = norm_text.split("\n")
    filtered_lines = msvdd_bloc.resumes.munge.get_filtered_text_lines(norm_text)
    assert isinstance(filtered_lines, list)
    assert len(filtered_lines) < len(lines)
    assert not filtered_lines[-1].isdigit()
