FIELD_SEPS = (":", ";", ",", "|")
FIELD_SEP_DTS = ("-", "–", "to")
FIELD_SEP_PREPS = ("in",)
FIELD_SEP_SMS = (",", ";")
FIELD_LABEL_SEPS = (":", "-")
LEFT_BRACKETS = ("(", "[")
RIGHT_BRACKETS = (")", "]")

DIRECTIONS = (
    "North", "South", "East", "West",
    "Northeast", "Northwest", "Southeast", "Southwest",
)
SEASONS = ("Spring", "Summer", "Fall", "Winter")

SCHOOL_DEGREES = (
    "Diploma", "High School Diploma", "Honor's Diploma",
    "GED", "G.E.D.",
)
SCHOOL_TYPES = (
    "Academy",
    "High",
    "High School",
    "Institute",
    "School",
    "School of Fine Arts",
    "Secondary School",
)

UNIVERSITY_DEGREES = (
    "Associate", "Associate Degree",
    "AA", "A.A.", "Associate of Arts",
    "AE", "A.E.", "Associate of Engineering",
    "APS", "A.P.S.", "Associate of Political Science",
    "AS", "A.S.", "Associate of Science",
    "AAS", "A.A.S.", "Associate of Applied Science",
    "Bachelor", "Bachelor's", "Bachelor's Degree",
    "B.Arch.", "Bachelor of Architecture",
    "BA", "B.A.", "Bachelor of Arts",
    "BBA", "B.B.A.", "Bachelor of Business Administration",
    "BCS", "BS CS", "B.Sc. CS", "BCompSc", "Bachelor of Computer Science",
    "BFA", "B.F.A.", "Bachelor of Fine Arts",
    "BS", "B.S.", "B.Sc.", "BSc", "Bachelor of Science",
    "Master", "Master's", "Master's Degree",
    "MA", "M.A.", "Master of Arts",
    "MBA", "M.B.A.", "Master of Business Administration",
    "MFA", "M.F.A.", "Master of Fine Arts",
    "M.Phil.", "Master of Philosophy",
    "MS", "M.S.",  "Master of Science",
    "Doctorate", "Doctorate Degree",
    "Ed.D.", "Doctor of Education",
    "JD", "J.D.", "Juris Doctor",
    "MD", "M.D.", "Doctor of Medicine",
    "PhD", "Ph.D.", "Doctor of Philosophy",
)
UNIVERSITY_SUBUNITS = ("College", "Institute", "School", "Department", "Dept.")
UNIVERSITY_SUFFIXES = (
    "Institute of Technology",
)
UNIVERSITY_TYPES = (
    "University", "College",
    "State University", "State College",
    "Polytechnic University", "Community College"
)

STUDY_SUBUNITS = ("Major", "Minor", "Concentration", "Emphasis")
AREAS_OF_STUDY = (
    "Humanities",
    "Anthropology",
    "Archaeology",
    "History",
    "Linguistics and Languages",
    "Philosophy",
    "Religion",
    "The Arts",
    "Culinary Arts",
    "Literature",
    "Performing Arts",
    "Visual Arts",
    "Social Sciences",
    "Economics",
    "Geography",
    "Interdisciplinary Studies",
    "Area Studies",
    "Ethnic and Cultural Studies",
    "Gender and Sexuality Studies",
    "Organizational Studies",
    "Political Science",
    "Psychology",
    "Sociology",
    "Natural Sciences",
    "Biology",
    "Chemistry",
    "Earth Sciences",
    "Physics",
    "Space Sciences",
    "Astronomy",
    "Formal Sciences",
    "Computer Sciences", "Computer Science",  # HACK: add singular CS
    "Logic",
    "Mathematics",
    "Pure Mathematics",
    "Applied Mathematics",
    "Statistics",
    "Systems Science",
    "Professions and Applied Sciences",
    "Agriculture",
    "Architecture and Design",
    "Business",
    "Divinity",
    "Education",
    "Engineering and Technology",
    "Environmental Studies and Forestry",
    "Family and Consumer Science",
    "Human Physical Performance and Recreation",
    "Journalism, Media Studies and Communication",
    "Law",
    "Library and Museum Studies",
    "Medicine",
    "Military Sciences",
    "Public Administration",
    "Public Policy",
    "Social Work",
    "Transportation",
)

COURSE_SUBJECTS = (
    "Accounting and Informational Systems",
    "Acting",
    "Aeronautics and Astronautics",
    "Agricultural Science",
    "Animal Science",
    "Anthropology",
    "Applied Math",
    "Applied Mathematical Sciences",
    "Aquatic and Fishery Sciences",
    "Architectural Design",
    "Art",
    "Art History",
    "Astronomy",
    "Astronomy",
    "Atmospheric Sciences",
    "Biochemistry",
    "Bioengineering",
    "Bioengineering",
    "Biology",
    "Biology",
    "Bioresource Science and Engineering",
    "Botany",
    "Business Administration",
    "Chemical Engineering",
    "Chemistry",
    "Cinematography",
    "City Planning",
    "Civil and Environmental Engineering",
    "Classics",
    "Communication*",
    "Comparative Literature",
    "Comparative Literature",
    "Computer Engineering and Computer Science",
    "Construction Management",
    "Costume Design",
    "Criminal Science and Forensics",
    "Criminology",
    "Dance",
    "Design",
    "Digital Arts",
    "Drama",
    "Earth and Space Science",
    "Earth and Space Sciences",
    "Ecology",
    "Economics",
    "Economics",
    "Education",
    "Electrical Engineering",
    "English",
    "Entomology",
    "Entrepreneurship",
    "Environmental Science",
    "Environmental Studies",
    "Environmental Studies and Policy",
    "Ethnic and Gender Studies",
    "Ethnomusicology",
    "Film Studies",
    "Finance",
    "Food Science",
    "Foreign Language and Literature",
    "Forestry and Wildlife Management",
    "Genetics",
    "Geography",
    "Geology",
    "Geology",
    "Graphic Design",
    "Health Informatics",
    "History",
    "History Of Music",
    "Industrial Engineering",
    "Informatics",
    "Informatics",
    "International Business",
    "International Studies",
    "Kinesiology",
    "Library Science",
    "Linguistics",
    "Management",
    "Marine Biology",
    "Marketing",
    "Materials Science and Engineering",
    "Mathematics",
    "Mechanical Engineering",
    "Medical Technology",
    "Microbiology",
    "Molecular Biology",
    "Music",
    "Music Composition",
    "Music Education",
    "Music Performance",
    "Neurobiology",
    "Nursing",
    "Nutrition Science",
    "Oceanography",
    "Oceanography and Marine Biology",
    "Philosophy",
    "Physics",
    "Physiology",
    "Political Science",
    "Prop Production",
    "Psychology",
    "Psychology",
    "Recording Technology",
    "Religious Studies",
    "Resource Management",
    "Rhetoric",
    "Social Justice",
    "Social Welfare",
    "Sociology",
    "Speech and Hearing Sciences",
    "Sports Medicine",
    "Stage Design",
    "Statistics",
    "Technical Communication",
    "Theater Management",
    "Video Game Design",
    "Viticulture and Enology",
    "Writing",
)
COURSE_PREFIXES = (
    "Introductory", "Intro to", "Intermediate", "Advanced", "Elementary",
    "Contemporary", "Modern", "21st Century", "20th Century", "Classical",
    "Perspectives on",
)
COURSE_SUFFIXES = (
    "1", "2", "I", "II", "101", "201",
)

FIELD_LABEL_COURSES = (
    "Courses", "Coursework", "Course Work",
    "Relevant Courses", "Relevant Coursework", "Relevant Course Work",
    "Recent Courses", "Recent Coursework", "Recent Course Work",
    "Courses Completed",
)
FIELD_LABEL_GRAD_DATES = (
    "Graduation", "Graduating",
    "Graduated", "Expected Graduation", "Expected",
    "Class of",
)
FIELD_LABEL_GPAS = (
    "GPA", "Cumulative GPA", "Current GPA", "Grade Point Average",
)
