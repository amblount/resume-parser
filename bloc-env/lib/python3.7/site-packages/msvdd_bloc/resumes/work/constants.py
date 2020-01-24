FIELD_SEPS = ("–", "-", "|", "�")
FIELD_SEP_DTS = ("-", "–", "to")
FIELD_SEP_PREPS = ("for", "at")
FIELD_SEP_SMS = (",", ";")

PUNCT_MID_SENTENCE = (",", ";", ":", "—")

SEASONS = ("Spring", "Summer", "Fall", "Winter")

COMPANY_NAMES = (
    "ANGI Homeservices Inc.", "ASOS.com", "AT&T", "Adobe", "Airbnb", "Albertsons", "Alibaba",
    "Alphabet Inc.", "Amazon", "Apple Inc.", "Aramark", "B2W", "Baidu", "Berkshire Hathaway",
    "Bet365", "Bloomberg L.P.", "Booking", "ByteDance", "Chewy",
    "Cognizant Technology Solutions", "Copart", "DHL", "Dell Technologies", "Expedia",
    "Facebook", "FedEx", "Flipkart", "Foxconn", "General Electric", "GoDaddy", "Google",
    "Groupon", "Grubhub", "HCA Healthcare", "HP Inc.", "Hitachi", "Home Depot", "Huawei",
    "IBM", "Intel", "International Business Machines", "J.P. Morgan Chase", "JD.com",
    "Kroger", "LG Electronics", "Lowe's", "Lyft", "Mail.Ru", "Match Group", "McDonald's",
    "Meituan-Dianping", "Microsoft", "Naver", "NetEase", "Netflix", "New egg", "Overstock",
    "Panasonic", "Paypal", "PepsiCo", "Rakuten", "Sabre Corporation", "Salesforce.com",
    "Samsung Electronics", "ServiceNow", "Shopify", "Snap", "Sony", "Spotify", "Starbucks",
    "Stitch Fix", "TJX", "Target Corporation", "Tencent", "Tesla", "The Stars Group",
    "TripAdvisor", "Twitter", "Uber", "United Parcel Service", "UnitedHealth Group",
    "Walgreens Boots Alliance", "Walmart", "Wayfair", "Wells Fargo", "Wish", "Workday",
    "Yandex", "Yum! Brands", "Zalando", "Zillow", "eBay",
)
"""
Sources:
    - https://en.wikipedia.org/wiki/List_of_largest_United_States-based_employers_globally
    - https://en.wikipedia.org/wiki/List_of_largest_Internet_companies
    - https://en.wikipedia.org/wiki/List_of_largest_technology_companies_by_revenue
"""
COMPANY_TYPES = (
    "Corporation", "Incorporated", "Corp.", "Inc.", "Ltd.",
    "Company", "Co.", "LLC", "L.L.C.", "LC", "L.C.",
    "Group", "Co-Op", "Bank", "Center", "Association", "Chapter",
    "University", "College", "Institute", "Academy", "School", "Lab", "Hospital",
)
COMPANY_MODIFIERS = (
    "U.S.", "National", "Regional", "Professional",
)
POSITION_LEVELS = (
    "Intern", "Junior", "Associate", "Senior", "Lead", "Sr.", "Jr.",
    "Manager", "Supervisor", "Director",
    "Head", "Vice-President", "Chief",
)
POSITION_TYPES = (
    "Accountant", "Administrator", "Advisor", "Agent", "Analyst", "Apprentice",
    "Architect", "Assistant", "Associate", "Auditor", "Bookkeeper", "Buyer",
    "Captain", "Cashier", "Clerk", "Coach", "Coder", "Collector", "Consultant",
    "Contractor", "Coordinator", "Copywriter", "Counselor", "Designer",
    "Developer", "Director", "Doctor", "Driver", "Editor", "Educator", "Engineer",
    "Estimator", "Evaluator", "Examiner", "Executive", "Expert", "Fellow",
    "Handler", "Inspector", "Instructor", "Intern", "Interviewer", "Investigator",
    "Laborer", "Leader", "Liaison", "Manager", "Merchandiser", "Nurse", "Officer",
    "Operator", "Pilot", "Planner", "President", "Processor", "Professor",
    "Programmer", "Receptionist", "Recruiter", "Representative", "Researcher",
    "Reviewer", "Salesperson", "Scheduler", "Scientist", "Secretary", "Specialist",
    "Strategist", "Supervisor", "Support", "Teacher", "Technician", "Technologist",
    "Temp", "Therapist", "Trader", "Trainee", "Trainer", "Treasurer", "Trustee", "Tutor",
    "Underwriter", "Webmaster", "Worker", "Writer", "Volunteer",
)

TEXT_SAMPLES = (
    "Backend engineer speeding login times for Amazon Online Payroll customers using Java "
    "Testing comprehensive user interfaces on the frontend using automation technologies such as Selenium and ReactJS based frameworks "
    "Worked with the software automation team using dynamic technologies such as .NET framework, C#, Visual Studio, and Angular 2 Javascript Framework to develop automated software used by Google engineers "
    "Created and maintained automation tools used to eliminate manual tasks otherwise performed by individuals "
    "Created comprehensive unit test plans and test cases in Selenium and javascript frameworks "
    "Worked on user testing, project management, error handling, and back-end development "
    "Participated in a week-long leadership camp that focused on \"Leading with Integrity\" "
    "Profiled the performance of a critical API that is responsible for ingesting member eligibility data "
    "Created an internal tool for operations team members to manage data patches (Angular, SASS) "
    "Implemented a test-ready version of SSO into our employer portals "
    "Refactored miscellaneous parts of our main backend service to improve code quality and maintainability "
    "Developed method to implement Kerberos authentication schema for in-house developer tool. "
    "Developed wrapper of git with hooks for local commits that performed static code analysis, security analysis, and config checks allowing for continuous integration and deployment. "
    "Designed pilot application for national market simulating the digital payment workflow with Paypal APIs. "
    "Designed, built, and tested internal web-based automation interface using MEAN stack technologies. "
    "Designed reusable user interface components and services using Angular and Typescript. "
    "Built scalable RESTFUL APIs using Typescript and NodeJS. "
    "Developed Python database upload utility for uploading mock data. "
    "Implemented over 10 graphs which call different API services that monitor DDOS, data centers, packet traffic, latency, CPU usage, and overall traffic hitting Twitter's website. "
    "Trained on triaging horizontal functions that deal with distributed systems, latency, error in spikes on services, connection stacking on Load Balancers, and dips to business metrics. "
    "Developing new swift iOS application "
    "Using Lottie animation framework to implement dynamic animations across screens "
    "Full stack web development on the main Dashboard product "
    "Worked inside the Database Cloud of Pets, Inc. infrastructure "
    "Created a web application for other Food, Co. engineers to run database qualification tests on a custom testing platform "
    "Tools used: Python, Django, Flask, Jenkins, Semantic UI, jQuery, various JavaScript libraries "
    "Worked with speech-to-text APIs to create front-end prototypes of search engines that leverage voice recognition technologies. "
    "Created an interactive SMS chatbot that answers common U.S. immigration and naturalization questions. Developed with Node.js, Express, and MongoDB. "
    "restructured how inventory was handled for stores and pop-up shops "
    "trained new hires for transition into new international distribution center "
    "Designed and implemented a medical record inbox and record viewer with auto-complete medical record search and customizable UI in React "
    "Worked on the admin dashboard, user authentication, audit logs, and record upload using Ruby on Rails and Google Cloud "
    "Worked on Chrome Extension that integrates service with EMR/EHR systems, such as Athena "
    "Managed product deadlines, and lead the development team's goals "
    "Using NLP techniques to detect code duplication, and near duplicates. "
    "Used visual analytics, computer vision, andML/DL techniques for image processing. "
    "Accuracy analysis of different deep-learning algorithms "
    "Integrated authentication services that suite the requirements of the newly built API. "
    "Built analysis tools to output static images of entire point cloud, static on number of points. "
    "Interviewed customer service agents to identify new care tool features to ease daily tasks "
    "Expanded proxy layer between platforms to maintain care tool during data migration "
    "Automated data cleaning and validation  processes with R, and Excel; documented new data sets "
    "Publishing an academic journal article on the framework that emerged out of the Scholars program on teaching data science at the high school level in underrepresented communities "
    "Refined and developed new program materials using R, incorporating feedback from pilot phase students "
    "Researched and implemented Wordpress plugin into React Native Android. "
    "Aided in the implementation of mobile data API. "
    "Assisted with completion in the simplification of handled exception source code on Android and iOS. "
    "Worked on multiple future processer projects "
    "Led the redesign of web page with Design and Marketing teams to enhance user exploration of company offerings "
    "Drove key end-to-end components such as Summary Page, Category List Items, and more to increase overall user conversion "
    "Increased user visibility and interaction by 32% on product description pages such as courses, degrees, and specializations "
    "Assisted in making improvements to the company website using various technologies like JavaScript, React, MobX and Pug. "
    "Collaborated with a team of four to organize events that focused on building a community of remarkable women in tech. "
    "Integrated with social media REST APIs to source profile information. "
    "Currently working with the DevOps Eng team comprised of 5 engineers and am responsible for the systems and procedures involved in the stable operation of the platform "
    "Creating and maintaining the tools used for provisioning services and running releases; current tasks include managing and productionizing forthcoming open-source cloud monitoring tools, Icarus and Graphmaker, via Kubernetes "
    "Identified risk areas in a Clock / Reset definition for CPU metastability "
    "Interned at Knight College campus in Tuckahoe Kentucky "
    "Completed a 3-week programming training class led by software engineers from SoftMax. "
    "Intern at the Experimentations team, helping build Drop's A/B testing tools "
    "Migrated the current ViewModels and code in C# to React + Flux using Typescript and SatchelJS "
    "Gathering requirements from superusers of current third-party application in order to prevent feature creep "
    "Monitor influx of tickets on Jira platform and respond to bugs that are assigned by management team "
)
"""
str: Samples of text taken from real résumés' work sections (with any PII removed/changed),
for use in training a Markov model in fake data generation.
"""
