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
 "Abkhazian", "Afar", "Afrikaans", "Akan", "Albanian", "Amharic", "Arabic",
 "Aragonese", "Armenian", "Assamese", "Avaric", "Avestan", "Aymara", "Azerbaijani",
 "Bambara", "Bashkir", "Basque", "Belarusian", "Bengali", "Bihari",
 "Bislama", "Bosnian", "Breton", "Bulgarian", "Burmese", "Catalan, Valencian",
 "Chamorro", "Chechen", "Chichewa", "Chewa", "Nyanja", "Chinese", "Chuvash", "Cornish",
 "Corsican", "Cree", "Croatian", "Czech", "Danish", "Divehi", "Dhivehi", "Maldivian",
 "Dutch, Flemish", "Dzongkha", "English", "Esperanto", "Estonian", "Ewe", "Faroese",
 "Fijian", "Finnish", "French", "Fulah", "Galician", "Georgian", "German",
 "Greek", "Guarani", "Gujarati", "Haitian", "Haitian Creole", "Hausa",
 "Hebrew", "Herero", "Hindi", "Hiri Motu", "Hungarian", "Interlingua", "Indonesian",
 "Interlingue", "Irish", "Igbo", "Inupiaq", "Ido", "Icelandic",
 "Italian", "Inuktitut", "Japanese", "Javanese", "Kalaallisut", "Greenlandic",
 "Kannada", "Kanuri", "Kashmiri", "Kazakh", "Central Khmer", "Kikuyu", "Gikuyu",
 "Kinyarwanda", "Kirghiz", "Kyrgyz", "Komi", "Kongo", "Korean", "Kurdish",
 "Kuanyama", "Kwanyama", "Latin", "Luxembourgish", "Letzeburgesch", "Ganda",
 "Limburgan", "Limburger", "Limburgish", "Lingala", "Lao", "Lithuanian", "Luba-Katanga",
 "Latvian", "Manx", "Macedonian", "Malagasy", "Malay", "Malayalam", "Maltese",
 "Maori", "Marathi", "Marshallese", "Mongolian", "Nauru", "Navajo", "Navaho",
 "North Ndebele", "Nepali", "Ndonga", "Norwegian Bokmål", "Norwegian Nynorsk",
 "Norwegian", "Sichuan Yi", "Nuosu", "South Ndebele", "Occitan", "Ojibwa",
 "Church Slavic", "Old Slavonic", "Church Slavonic", "Old Bulgarian", "Old Church Slavonic",
 "Oromo", "Oriya", "Ossetian", "Ossetic", "Punjabi", "Panjabi", "Pali", "Persian",
 "Polish", "Pashto", "Pushto", "Portuguese", "Quechua", "Romansh", "Rundi",
 "Romanian", "Moldavian", "Moldovan", "Russian", "Sanskrit", "Sardinian", "Sindhi",
 "Northern Sami", "Samoan", "Sango", "Serbian", "Gaelic", "Scottish Gaelic", "Shona",
 "Sinhala", "Sinhalese", "Slovak", "Slovenian", "Somali", "Southern Sotho",
 "Spanish", "Castilian", "Sundanese", "Swahili", "Swati", "Swedish", "Tamil", "Telugu",
 "Tajik", "Thai", "Tigrinya", "Tibetan", "Turkmen", "Tagalog", "Tswana",
 "Tonga", "Turkish", "Tsonga", "Tatar", "Twi", "Tahitian",
 "Uighur", "Uyghur", "Ukrainian", "Urdu", "Uzbek", "Venda", "Vietnamese", "Volapük",
 "Walloon", "Welsh", "Wolof", "Western Frisian", "Xhosa", "Yiddish", "Yoruba",
 "Zhuang", "Chuang", "Zulu",
)
"""
Tuple[str]: Set of human languages using the ISO standard.

Source: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
"""

HOBBIES = (
    "Acting", "Aerobics", "Amateur Radio", "Animal Care", "Antiques", "Aquariums",
    "Archaeology", "Archery", "Architecture", "Aromatherapy", "Astrology", "Astronomy",
    "Autographs", "Badge Collecting", "Badminton", "Baking", "Ballet", "Base Jumping",
    "Baseball", "Basketball", "Beach", "Bee Keeping", "Bicycling", "Billiards", "Boating",
    "Bowling", "Camping", "Church Activities", "Computer", "Cooking", "Crafts", "Dancing",
    "Eating Out", "Entertaining", "Exercise", "Family Time", "Fashion", "Fencing", "Films",
    "Fish Keeping", "Fishing", "Fitness", "Flower Arranging", "Football", "Fossils",
    "Frisbee", "Gardening", "Genealogy", "Going to the Movies", "Golf",
    "Greeting Card Collecting", "Greyhound Racing", "Handball", "Handwriting", "Hiking",
    "History", "Hockey", "Home Brewing", "Horseback Riding", "Housework", "Hunting",
    "Karaoke", "Kayaking", "Listening to Music", "Motorcycling", "Ornithology", "Paintball",
    "Painting", "Papercraft", "Photography", "Playing Cards", "Playing Music", "Poker",
    "Polo", "Poole", "Post Cards", "Pottery", "Psychology", "Quilting", "RC Model Aircrafts",
    "RC Model Boats", "RC Model Cars", "Reading", "Reflexology", "Relaxing", "Riddles",
    "Robotics", "Rock Climbing", "Rock Music", "Roller Skating", "Running", "Sewing",
    "Shopping", "Skiing", "Sleeping", "Socializing", "Swimming", "Team Sports", "Tennis",
    "Theater", "Traveling", "Volunteer Work", "Walking", "Watching Sports", "Watching TV",
    "Working on Cars", "Writing",
 )
