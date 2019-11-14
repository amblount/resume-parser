GROUP_SEPS = (":", "-", "–")
ITEM_SEPS = (",", ";")
ITEM_SEP_ANDS = ("and", "&")
LEVEL_PREPS = ("in", "with", "to", "of")
LEFT_BRACKETS = ("(", "[")
RIGHT_BRACKETS = (")", "]")

LEVELS = (
    "advanced", "intermediate", "beginner",
    "experienced", "proficient", "exposed", "exposure",
    "basic", "familiar", "fluent", "native",
)
GROUP_NAMES = (
    "Programming Languages", "Languages", "Programming",
    "Web Frameworks", "Web Frameworks/Tools", "Tools",
    "Frameworks and Tools", "Tools & Frameworks", "Frameworks & Tools",
    "Software", "Databases", "Technologies",
    "Technical Skills", "Domain Knowledge",
    "Interests", "Hobbies",
)
PROGRAMMING_LANGUAGES = (
    "Java", "Python", "C", "C++", "C/C++", "C#", "Objective-C", "Objective C",
    "SQL", "Ruby", "MATLAB", "Go", "Swift", "Perl", "R", "Visual Basic", "Scala", "PHP",
    "HTML", "HTML5", "CSS", "HTML/CSS", "JavaScript", "TypeScript", "Groovy",
    "Processing", "Sass", "OCaml",
)
DATABASES = (
    "PostgreSQL", "Postgres", "MongoDB", "Mongo DB",
    "Redshift", "MySQL", "MariaDB", "SQLite", "NoSQL", "GraphQL",
    "SQLAlchemy", "DynamoDB", "Elasticsearch", "Redis", "SQL Server", "Oracle",
    "Cassandra", "Memcached", "IBM DB2", "Neo4j",
)
DEV_BE = (
    "Airflow", "Bash", "Docker", "Kafka", "Apache Kafka", "Chef", "Kubernetes", "Hadoop",
    "Kibana", "Data Structures", "Data Architecture",
)
DEV_DS = (
    "TensorFlow", "OpenCV", "PyTorch", "ArcGIS", "Spark", "PyData",
    "Machine Learning", "Supervised Machine Learning", "Unsupervised Machine Learning",
    "Deep Learning", "Big Data", "Forecasting", "Web Analytics",
    "Time Series Analysis", "TSA", "Natural Language Processing", "NLP",
    "Network Analysis", "Algorithms", "Data Analysis", "Data Pipelines",
)
DEV_FE = (
    "React", "ReactJS", "React Native", "Node.js", "Node JS", "Angular", "Angular JS",
    "Express JS", "jQuery", "LESS", "AJAX", "Electron", "Selenium",
    "Rest APIs", "CRUD", "Ruby on Rails", "Django", "Flask",
)
DEV_TECHNIQUES = (
    "agile development", "parallel programming", "networking", "web development",
    "unit testing", "cyber security", "SEO",
)
DEV_TOOLS = (
    "Git", "GitHub", "Version Control",
    "Sublime", "Atom", "VS Code", "Eclipse", "IDE", "Shell", "Terminal",
    "IPython Notebooks", "Jupyter Notebooks", "RStudio",
    "LaTeX", "Markdown", "JSON", "XML",
    "WordPress", "Heroku", "Jenkins", "VMWare",
    "AWS", "Amazon Web Services", "GCP", "Google Cloud Platform", "Google Cloud",
    "Microsoft Azure",
)
DEV_MIX = (
    DEV_BE + DEV_DS + DEV_FE
    + DEV_TECHNIQUES + DEV_TOOLS
    + DATABASES + PROGRAMMING_LANGUAGES
)

SOFTWARE = (
    "Linux", "Unix", "Windows", "Mac OS", "macOS", "Android", "iOS", "Arduino",
    "Adobe Photoshop", "Adobe Illustrator", "Adobe InDesign", "Autodesk Maya",
    "Microsoft Office", "Microsoft Word", "Microsoft Excel",
    "JIRA", "Trello", "Asana",
)
HUMAN_LANGUAGES = (
    "Chinese", "Mandarin", "English", "Spanish", "Arabic", "Bengali", "Hindi", "Russian",
    "Portuguese", "Japanese", "German", "Javanese", "Korean", "French", "Turkish",
    "Marathi", "Tamil", "Italian", "Urdu", "Gujarati", "Polish", "Ukrainian", "Persian",
    "Malayalam", "Kannada", "Oriya", "Panjabi", "Romanian", "Bhojpuri", "Azerbaijani",
    "Maithili", "Hausa", "Burmese", "Serbo-Croatian", "Awadi", "Thai", "Dutch",
    "Yoruba", "Sindhi",
)
HOBBIES = (
    "Bowling", "Karaoke", "Kayaking", "Swimming", "Fishing", "Rock Climbing",
)
