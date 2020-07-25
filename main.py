from datetime import date
from enum import Enum, auto
from io import StringIO
from textwrap import dedent
from typing import List, NamedTuple, Optional


class Contacts(NamedTuple):
    email: str
    phone: str
    github: str
    gitlab: str
    skype: str
    web: str


class Address(NamedTuple):
    country: str
    city: str


class EducationLevel(Enum):
    # TODO
    TVET = auto()  # Technical and Vocational Education and Training
    BachelorsDegree = auto()
    MastersDegree = auto()


class YearInterval(NamedTuple):
    year_from: int
    year_to: int


class EducationPlace(NamedTuple):
    place: str
    speciality: str
    level: EducationLevel
    then: YearInterval


class Month(NamedTuple):
    year: int
    month: int


class MonthInterval(NamedTuple):
    month_from: Month
    month_to: Optional[Month]


class WorkingPlace(NamedTuple):
    place: str
    position: str
    then: MonthInterval
    description: str
    achivements: List[str]
    keywords: List[str]


class LanguageLevel(Enum):
    Beginner = auto()
    Intermediate = auto()
    Advanced = auto()
    Fluent = auto()
    Native = auto()


class Language(NamedTuple):
    name: str
    level: LanguageLevel


class SalaryPeriod(Enum):
    Annual = auto()
    Monthly = auto()


class SalaryUnit(Enum):
    USD = auto()
    RUB = auto()


class Salary(NamedTuple):
    period: SalaryPeriod
    unit: SalaryUnit
    amount: int


class Applicant(NamedTuple):
    name: str
    desired_salary: Salary
    birthdate: date
    contacts: Contacts
    address: Address
    education: List[EducationPlace]
    experience: List[WorkingPlace]
    languages: List[Language]
    skills: List[str]
    hobbies: List[str]
    wishes: List[str]


class Position(NamedTuple):
    name: str
    skills: List[List[str]]


class Resume(NamedTuple):
    applicant: Applicant
    position: Position

    def to_latex(self) -> str:
        result = StringIO()

        result.write(d(r"""
            \documentclass[11pt, a4paper]{minimal}
            \usepackage[english,russian]{babel}
            \begin{document}
                Resume here
            \end{document}
        """))

        return result.getvalue()


def d(text: str) -> str:
    """ Dedents text and removes unnecessary newlines """

    return dedent(text).strip()


me = Applicant(
    name="Denis Gruzdev",
    birthdate=date(1993, 7, 31),
    desired_salary=Salary(
        period=SalaryPeriod.Annual,
        unit=SalaryUnit.USD,
        amount=90000,  # ≈ 250000 Rub for 30% TAX
    ),
    contacts=Contacts(
        email="codingjerk@gmail.com",
        phone="79999767890",
        github="codingjerk",
        gitlab="codingjerk",
        skype="live:codingjerk",
        web="codingjerk.dev",
    ),
    address=Address(
        country="Russia",
        city="Moscow",
    ),
    education=[
        EducationPlace(
            place="Moscow College of Railway Transport",
            speciality="Automatic Information Processing and Control Systems",
            level=EducationLevel.TVET,
            then=YearInterval(2011, 2014),
        ),
        EducationPlace(
            place="Moscow Power Engineering Institute",
            speciality="Computer Science and Engineering",
            level=EducationLevel.BachelorsDegree,
            then=YearInterval(2014, 2017),
        ),
        EducationPlace(
            place="Moscow Power Engineering Institute",
            speciality="Applied Mathematics and Informatics",
            level=EducationLevel.MastersDegree,
            then=YearInterval(2020, 2022),
        ),
    ],
    experience=[
        WorkingPlace(
            place="Navigator Bank",
            position="Junior Software Developer",
            then=MonthInterval(Month(2010, 7), Month(2012, 12)),
            description=d("""
                I started working here half-time, just after I finished a school.
                We worked on accounting system for money transfers (Unistream, CONTACT, Western Union, KoronaPay) using Delphi and C++ as our primary programming languages paired with FoxPro database.
                Even on half-time job I've learned a lot.
            """),
            achivements=[
                "Improved performance of legacy report generation system",
                "Extended accounting system with client database module",
                "Added autocompletion feature to input forms",
            ],
            keywords=[
                "Delphi",
                "C++",
                "FoxPro",
            ],
        ),
        WorkingPlace(
            place="Central Scientific Research Institute of Chemistry and Mechanics",
            position="Software Developer (Computer Vision)",
            then=MonthInterval(Month(2014, 6), Month(2015, 4)),
            description=d("""
                It was a very interesting job with embedded devices, computer vision and a lot of creativity.
                I've worked on classified goverment projects, so I can't tell the details.
            """),
            achivements=[
                "Developed a video translation module for computer vision system of unmanned aerial vehicle",
                "Created a tool to monitor and control our embedded devices",
                "Created it's mobile version with C++ and Android NDK",
                "Trained a junior developer and taught him basics of computer vision",
            ],
            keywords=[
                "C/C++",
                "Python",

                "Qt",
                "OpenCV",
                "Embedded Programming",
                "Android NDK",

                "Computer Vision",
            ],
        ),
        WorkingPlace(
            place="Paragon Software",
            position="Software Developer",
            then=MonthInterval(Month(2015, 4), Month(2016, 10)),
            description=d("""
                We have been creating educational software, such as interactive schoolbooks and interactive learning boards for Mathematics, Physics, Geographics, etc.
            """),
            achivements=[
                "Writed an integration system to convert existing e-books to our format, which allowed us to increase typists productivity",
                "Created an internal package manager from scratch",
                "Increased code coverage to about 100% in all projects",
                "Mentored trainees and taught them until they became our junior developers",
            ],
            keywords=[
                "C++",
                "Python",
                "JavaScript/CoffeeScript",
                "Node.js",

                "wxWidgets",
                "Box2D",
                "XPath",
                "Selenium",
                "Electron",

                "Data Mining",
            ],
        ),
        WorkingPlace(
            place="Freelance",
            position="Fullstack Web Developer",
            then=MonthInterval(Month(2017, 1), Month(2019, 4)),
            description=d("""
                I worked with customers from different countries on international freelance platform.
                In the main I've accepted small tasks related to web, automation or data mining.
                As a result in additional to getting a lot of skills I've learned time management and improved my communication skills.
            """),
            achivements=[
                "Created queue-based image processing system for DeepDream iOS application",
                "Fixed minor issues in 30+ web sites",
                "Wrote data mining tools and web scrappers for 20+ sources",
            ],
            keywords=[
                "Python",
                "JavaScript/TypeScript",
                "Bash",

                "React.js",
                "Flask/Bottle",

                "Redis",
                "PostgreSQL",
                "MongoDB",

                "Kafka",
                "RabbitMQ",

                "Web Development",
                "Automation",
                "Data Mining",
            ],
        ),
        WorkingPlace(
            place="Polymedia",
            position="Web/ETL Developer",
            then=MonthInterval(Month(2019, 4), None),
            description=d("""
                We created a buisness intelligence platform Visiology, integrated it with various data sources and customized it to customer needs.
                I've learned a lot about databases, OLAP-cubes. Learned how to improve uncultivated development process and how to lead small teams.
            """),
            achivements=[
                "Improved development process and overall products quality by introducing gitflow, continous integration, unit and smoke testing",
                "Improved performance of XML parsing by creating specialized XML parser as Python Extension Module with Rust",
                "Improved maintainability of several legact projects by rewriting from scratch and/or gradual refactoring",
                "Created several forecasting models using machine learning",
                "Mentored and trained a lot of junior Python and JavaScript developers and new employees",
                "Led a team of four developers for half a month",
            ],
            keywords=[
                "Python",
                "SQL",
                "JavaScript",

                "Data Warehouse",
                "OLAP",

                "Buisness Intelligence",
                "Web Development",
                "ETL",
            ],
        ),
    ],
    languages=[
        Language("Russian", LanguageLevel.Native),
        Language("English", LanguageLevel.Intermediate),
        Language("French", LanguageLevel.Beginner),
    ],
    skills=[
        "Time management (work-load handling, scheduling)",
        "Training/mentoring junior developers",
        "Gradual improvement of legacy code",
    ],
    hobbies=[
        "Learning Romance languages",
        "Drawing hands with pen",
        "Playing guitar",
        "Using Haskell and Rust",
        "Writing compilers",
    ],
    wishes=[
        "Learning new domains",
        "Working with awesome people",
        "Creating awesome product",
    ],
)


python_developer = Position(
    name="Python Developer",
    skills=[[
        "Python",
        "asyncio/aiohttp",
        "PEP8",
        "MyPy / typing",
    ], [
        "REST/RESUful API",
        "WebSocket",
    ], [
        "Tornado",
        "Django/DRF",
    ], [
        "RabbitMQ",
        "Celery",
    ], [
        "PostgreSQL",
        "MongoDB",
        "Redis",
    ], [
        "Linux",
        "Docker",
    ], [
        "Git",
        "Automated Testing",
        "Continious Integration",
    # ], [
    #     "Flask",
    #     "Bottle",
    #     "Pandas",
    #     "Numpy",
    #     "Selenium",
    #     "Squish",
    # ], [
    #     "C++",
    #     "Bash",
    #     "JavaScript",
    # ], [
    #     "Data Structures and Algorithms",
    ]],
)


latex = Resume(me, python_developer).to_latex()
print(latex)
