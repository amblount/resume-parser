import random as rnd

import faker


_GROUP_SEPS = (":", "-", "–")
_ITEM_SEPS = (",", ";")
_ITEM_SEP_ANDS = ("and", "&")
_LEVEL_PREPS = ("in", "with", "to", "of")

_LEVELS = (
    "advanced", "intermediate", "beginner",
    "experienced", "proficient", "exposed", "exposure",
    "basic", "familiar", "fluent", "native",
)
_GROUP_NAMES = (
    "Programming Languages", "Languages", "Programming",
    "Web Frameworks", "Web Frameworks/Tools", "Tools",
    "Frameworks and Tools", "Tools & Frameworks", "Frameworks & Tools",
    "Software", "Databases", "Technologies",
    "Technical Skills", "Domain Knowledge",
    "Interests", "Hobbies",
)
_PROGRAMMING_LANGUAGES = (
    "Java", "Python", "C", "C++", "C/C++", "C#", "Objective-C", "Objective C",
    "SQL", "Ruby", "MATLAB", "Go", "Swift", "Perl", "R", "Visual Basic", "Scala", "PHP",
    "HTML", "HTML5", "CSS", "HTML/CSS", "JavaScript", "TypeScript", "Groovy",
    "Processing", "Sass", "OCaml",
)
_DATABASES = (
    "PostgreSQL", "Postgres", "MongoDB", "Mongo DB",
    "Redshift", "MySQL", "MariaDB", "SQLite", "NoSQL", "GraphQL",
    "SQLAlchemy", "DynamoDB", "Elasticsearch", "Redis", "SQL Server", "Oracle",
    "Cassandra", "Memcached", "IBM DB2", "Neo4j",
)
_DEV_BE = (
    "Airflow", "Bash", "Docker", "Kafka", "Apache Kafka", "Chef", "Kubernetes", "Hadoop",
    "Kibana", "Data Structures", "Data Architecture",
)
_DEV_DS = (
    "TensorFlow", "OpenCV", "PyTorch", "ArcGIS", "Spark", "PyData",
    "Machine Learning", "Supervised Machine Learning", "Unsupervised Machine Learning",
    "Deep Learning", "Big Data", "Forecasting", "Web Analytics",
    "Time Series Analysis", "TSA", "Natural Language Processing", "NLP",
    "Network Analysis", "Algorithms", "Data Analysis", "Data Pipelines",
)
_DEV_FE = (
    "React", "ReactJS", "React Native", "Node.js", "Node JS", "Angular", "Angular JS",
    "Express JS", "jQuery", "LESS", "AJAX", "Electron", "Selenium",
    "Rest APIs", "CRUD", "Ruby on Rails", "Django", "Flask",
)
_DEV_TECHNIQUES = (
    "agile development", "parallel programming", "networking", "web development",
    "unit testing", "cyber security", "SEO",
)
_DEV_TOOLS = (
    "Git", "GitHub", "Version Control",
    "Sublime", "Atom", "VS Code", "Eclipse", "IDE", "Shell", "Terminal",
    "IPython Notebooks", "Jupyter Notebooks", "RStudio",
    "LaTeX", "Markdown", "JSON", "XML",
    "WordPress", "Heroku", "Jenkins", "VMWare",
    "AWS", "Amazon Web Services", "GCP", "Google Cloud Platform", "Google Cloud",
    "Microsoft Azure",
)
_DEV_MIX = (
    _DEV_BE + _DEV_DS + _DEV_FE
    + _DEV_TECHNIQUES + _DEV_TOOLS
    + _DATABASES + _PROGRAMMING_LANGUAGES
)

_SOFTWARE = (
    "Linux", "Unix", "Windows", "Mac OS", "macOS", "Android", "iOS", "Arduino",
    "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign", "Autodesk Maya",
    "Microsoft Office", "Microsoft Word", "Microsoft Excel",
    "JIRA", "Trello", "Asana",
)
_HUMAN_LANGUAGES = (
    "Chinese", "Mandarin", "English", "Spanish", "Arabic", "Bengali", "Hindi", "Russian",
    "Portuguese", "Japanese", "German", "Javanese", "Korean", "French", "Turkish",
    "Marathi", "Tamil", "Italian", "Urdu", "Gujarati", "Polish", "Ukrainian", "Persian",
    "Malayalam", "Kannada", "Oriya", "Panjabi", "Romanian", "Bhojpuri", "Azerbaijani",
    "Maithili", "Hausa", "Burmese", "Serbo-Croatian", "Awadi", "Thai", "Dutch",
    "Yoruba", "Sindhi",
)
_HOBBIES = (
    "Bowling", "Karaoke", "Kayaking", "Swimming", "Fishing", "Rock Climbing",
)


class Provider(faker.providers.BaseProvider):

    def database(self):
        return rnd.choice(_DATABASES)

    def dev_mix(self):
        return rnd.choice(_DEV_MIX)

    def group_name(self):
        return rnd.choice(_GROUP_NAMES)

    def group_sep(self):
        return "{ws}{sep}".format(
            ws="" if rnd.random() < 0.9 else " ",
            sep=(
                rnd.choices(_GROUP_SEPS, weights=[1.0, 0.5, 0.25], k=1)[0] if rnd.random() < 0.9
                else ""
            ),
        )

    def hobby(self):
        return rnd.choice(_HOBBIES)

    def human_language(self):
        return rnd.choice(_HUMAN_LANGUAGES)

    def item_sep(self):
        return "{sep}{ws}".format(
            sep=rnd.choices(_ITEM_SEPS, weights=[1.0, 0.2], k=1)[0],
            ws=" " * rnd.randint(1, 2),
        )

    def item_sep_and(self):
        return rnd.choices(_ITEM_SEP_ANDS, weights=[1.0, 0.2], k=1)[0]

    def level(self):
        return rnd.choice(_LEVELS)

    def level_prep(self):
        return rnd.choices(_LEVEL_PREPS, weights=[1.0, 0.4, 0.2, 0.1], k=1)[0]

    def newline(self):
        return "\n" if rnd.random() < 0.8 else "\n\n"

    def programming_language(self):
        return rnd.choice(_PROGRAMMING_LANGUAGES)

    def software(self):
        return rnd.choice(_SOFTWARE)

    def whitespace(self):
        return " " * rnd.randint(0, 3)
