from datetime import date, datetime
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
    linkedin: str
    web: str

    def beauty_phone(self) -> str:
        p1 = self.phone[0]
        p2 = self.phone[1:4]
        p3 = self.phone[4:7]
        p4 = self.phone[7:9]
        p5 = self.phone[9:11]

        return f"+{p1} ({p2}) {p3}-{p4}-{p5}"


class Address(NamedTuple):
    country: str
    city: str


class EducationLevel(Enum):
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

    def age(self, at: date) -> int:
        return years_between(self.birthdate, at)


class Position(NamedTuple):
    name: str
    skills: List[List[str]]


class Resume(NamedTuple):
    applicant: Applicant
    position: Position

    def to_latex(self) -> str:
        generator = LatexGeneartor(self)
        return generator.generate()


def d(text: str) -> str:
    """ Dedents text and removes unnecessary newlines """

    return dedent(text).strip()


def is_date_before(test_date, point_date):
    if test_date.month < point_date.month:
        return True

    if test_date.month > point_date.month:
        return False

    return test_date.day < point_date.day


def years_between(from_date: date, to_date: date) -> int:
    rough_difference = to_date.year - from_date.year

    if is_date_before(to_date, from_date):
        return rough_difference - 1

    return rough_difference


class LatexGeneartor():
    def __init__(self, resume: Resume) -> None:
        self.resume = resume
        self.stream = StringIO()

    def write(self, text: str) -> None:
        self.stream.write(text)

    def write_line(self, line: str) -> None:
        self.write(line + "\n")

    def write_latex_header(self) -> None:
        self.write(d(r"""
            \documentclass[11pt, a4paper]{minimal}
            \usepackage[papersize={8.5in,11in}]{geometry}
            \usepackage[english,russian]{babel}
            \usepackage{hyperref}
            \usepackage{fontawesome}
        """))

    def write_age(self) -> None:
        now = datetime.now().date()
        age = self.resume.applicant.age(at=now)
        self.write_line(f"{age} years old")

    def write_phone(self) -> None:
        self.write_link_with_icon(
            url=f"tel:{self.resume.applicant.contacts.phone}",
            icon="phone",
            text=self.resume.applicant.contacts.beauty_phone(),
        )

    def write_email(self) -> None:
        self.write_text_with_icon(
            icon="envelope",
            text=self.resume.applicant.contacts.email,
        )

    def write_text_with_icon(self, icon: str, text: str) -> None:
        self.write(r"\faicon{%s}~%s" % (icon, text))

    def write_link_with_icon(self, url: str, icon: str, text: str) -> None:
        self.write(r"\href{%s}" % url)
        self.write("{")
        self.write_text_with_icon(icon, text)
        self.write("}")

    def write_github(self) -> None:
        username = self.resume.applicant.contacts.github
        self.write_link_with_icon(
            url=f"https://github.com/{username}",
            icon="github",
            text=username,
        )

    def write_gitlab(self) -> None:
        username = self.resume.applicant.contacts.gitlab
        self.write_link_with_icon(
            url=f"https://gitlab.com/{username}",
            icon="gitlab",
            text=username,
        )

    def write_skype(self) -> None:
        self.write_text_with_icon(
            icon="skype",
            text=self.resume.applicant.contacts.skype,
        )

    def write_linkedin(self) -> None:
        self.write_text_with_icon(
            icon="linkedin",
            text=self.resume.applicant.contacts.linkedin,
        )

    def write_web(self) -> None:
        site = self.resume.applicant.contacts.web
        self.write_link_with_icon(
            url=f"https://{site}",
            icon="globe",
            text=site,
        )

    def write_contacts(self) -> None:
        self.write_phone()
        self.write(" | ")
        self.write_email()
        self.write(" | ")
        self.write_github()
        self.write(" | ")
        self.write_gitlab()
        self.write(" | ")
        self.write_skype()
        self.write(" | ")
        self.write_linkedin()
        self.write(" | ")
        self.write_web()

    def write_header(self) -> None:
        self.write_line(self.resume.applicant.name)
        self.write_line("")
        self.write_line(self.resume.position.name)
        self.write_line("")
        self.write_age()
        self.write_line("")
        self.write_line(self.resume.applicant.address.country)
        self.write_line("")
        self.write_contacts()

    def write_skill(self, skill: str) -> None:
        self.write_line(fr"\item {skill}")

    def write_all_skills(self) -> None:
        self.write_line(r"\begin{itemize}")

        for skill in self.resume.applicant.skills:
            self.write_skill(skill)

        for skill_group in self.resume.position.skills:
            for skill in skill_group:
                self.write_skill(skill)

        self.write_line(r"\end{itemize}")

    def write_content(self) -> None:
        self.write_header()
        self.write_all_skills()
        # self.write_languages()
        # self.write_experince()
        # self.write_education()

    def write_document(self) -> None:
        self.write_line(r"\begin{document}")
        self.write_content()
        self.write_line(r"\end{document}")

    def generate(self) -> str:
        self.write_latex_header()
        self.write_document()

        return self.stream.getvalue()


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
        linkedin="codingjerk",
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
    ]],
)


latex = Resume(me, python_developer).to_latex()
print(latex)
