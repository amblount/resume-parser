FIELD_LABEL_SEPS = (":", "-")
FIELD_SEPS = ("|", "–", "-", ":", "•", "·", "Ÿ", "�", "⇧")
ITEM_SEPS = (",", ";")

FIELD_LABEL_ADDRS = ("Address", "Current Address")
FIELD_LABEL_EMAILS = ("Email", "E-mail")
FIELD_LABEL_PHONES = ("Phone", "Mobile", "Cell", "Tel.")
FIELD_LABEL_PROFILES = ("GitHub", "Twitter", "LinkedIn", "Portfolio")

PHONE_FORMATS = (
    "###-###-####", "###.###.####", "(###) ###-####", "### ###-####",
)
URL_SCHEMES = ("www.", "http://", "http://www.")

LOCATION_TAG_MAPPING = {
   'Recipient': 'recipient',
   'AddressNumber': 'address',
   'AddressNumberPrefix': 'address',
   'AddressNumberSuffix': 'address',
   'StreetName': 'address',
   'StreetNamePreDirectional': 'address',
   'StreetNamePreModifier': 'address',
   'StreetNamePreType': 'address',
   'StreetNamePostDirectional': 'address',
   'StreetNamePostModifier': 'address',
   'StreetNamePostType': 'address',
   'CornerOf': 'address',
   'IntersectionSeparator': 'address',
   'LandmarkName': 'address',
   'USPSBoxGroupID': 'address',
   'USPSBoxGroupType': 'address',
   'USPSBoxID': 'address',
   'USPSBoxType': 'address',
   'BuildingName': 'address',
   'OccupancyType': 'address',
   'OccupancyIdentifier': 'address',
   'SubaddressIdentifier': 'address',
   'SubaddressType': 'address',
   'PlaceName': 'city',
   'StateName': 'region',
   'ZipCode': 'postal_code',
}
"""
Dict[str, str]: Mapping of ``usaddress`` location tag to corresponding résumé schema field.
"""

TEXT_SAMPLES = (
    "I am currently an undergraduate senior at Georgia University pursuing an honors, dual degree in Physics & Electrical Engineering. I will graduate in June of 2017. My work experience includes a year's worth of internship between Foogle and Gacebook as a Project Manager and a Back-end Engineer. My skills include communication, resourcefulness, work ethic, adaptability, and attention to detail. I am looking for a full-time position at a company with a challenging, dynamic, and fast-paced environment with a strong team connection. "
    "3+ years of experience in HTML/CSS language "
    "Strong ability to work in and lead group projects"
    "Knowledge in computer architecture, including digital systems and computer organization "
    "Skilled at working under pressure and communicating ideas effectively "
    "Strong interest in field of Design and Computer Architecture "
    "A highly skilled, knowledgeable, and accomplished data science student with extensive knowledge of programming and computer applications seeking an opportunity in the field of information technology to utilize my programming skillset to help contribute to the success of a growing company. "
    "An internship that will help develop my skills in computer science and languages with an organization that I can make an impact at using my skills, creativity, and work ethic. "
    "I am a December 2015 graduate with interest in obtaining a future long-term industry position, where I can serve as a trusted advisor to my team and further advance my knowledge in software engineering, team development, and project management. "
    "I am a passionate second-year student enthusiastic to learn and explore more in the field of Information Technology and Software Development. I am currently seeking to continue building my skills and gaining hands-on, real-life experience in the tech industry. "
    "To acquire a software position in Computer Engineering that will utilize my interpersonal skills and experiences. "
    "Driven student who offers experience in Python, JavaScript, C++, and Perl with a passion to go into the field of engineering, computing, or Artificial Intelligence. Curious to gain more knowledge about the tech workspace and presents creative outlooks to different tasks. Provides innovative solutions to real world problems. Self-motivated and inspired to change the world through technology. "
    "An innovative problem solver that thrives in a forward-thinking company/institution operating in a team-based, leading industry and educational environment. I strive to create intuitive and beautiful user experiences from conception to implementation, while challenging myself with new learning skills and technologies. "
    "To obtain an back-end or mobile engineering internship granting me the opportunity to utilize and enhance technical and leadership skills, becoming a successful contributor and asset to the organization. "
    "Seeking a position as a Software Intern at ABC Corporation utilizing exceptional software engineering skills, and abilities and experiences gained through relevant education, projects, and internships to contribute to the ongoing success of company. "
    "Result-oriented engineering undergrad who is interested in Data Science and Machine Learning and would like to obtain a Software Engineering role that will allow me to utilize my technical and leadership skills to develop efficient technological solutions for the company. "
)
"""
str: Samples of text taken from real résumés' summary sections (with any PII removed/changed),
for use in training a Markov model in fake data generation.
"""
