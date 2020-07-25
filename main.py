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


class Month(NamedTuple):
    year: int
    month: int


class MonthInterval(NamedTuple):
    month_from: Month
    month_to: Month


class EducationPlace(NamedTuple):
    place: str
    speciality: str
    level: EducationLevel
    then: MonthInterval


class WorkingPlace(NamedTuple):
    place: str
    position: str
    then: MonthInterval
    achivements: List[str]


class LanguageLevel(Enum):
    Beginner = auto()
    Intermediate = auto()
    Advanced = auto()
    Fluent = auto()
    Native = auto()


class Language(NamedTuple):
    name: str
    level: LanguageLevel


class Applicant(NamedTuple):
    name: str
    birthdate: date
    contacts: Contacts
    address: Address
    education: List[EducationPlace]
    experience: List[WorkingPlace]
    languages: List[Language]
    skills: List[str]


class Position(NamedTuple):
    name: str
    skills: List[str]


class Resume(NamedTuple):
    applicant: Applicant
    position: Position

    def to_latex(self):
        pass


me = Applicant(
    name="Denis Gruzdev",
    birthdate=date(1993, 7, 31),
    contacts=Contacts(
        email="codingjerk@gmail.com",
        phone="+79999767890",
        github="codingjerk",
        gitlab="codingjerk",
        skype="live:codingjerk",
        web="codingjerk.dev",
    ),
    address=Address(
        country="Russia",
        city="Moscow",
    ),
    education=[],
    experience=[],
    languages=[
        Language("Russian", LanguageLevel.Native),
        Language("English", LanguageLevel.Intermediate),
    ],
    skills=[],
)


python_developer = Position(
    name="Python Developer",
    skills=[
        "Python",
        "Flask/Bottle",
        "Pandas/Numpy",
        "SQL",
    ],
)


latex = Resume(me, python_developer).to_latex()
print(latex)
