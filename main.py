from typing import NamedTuple, List
from enum import Enum, auto
from datetime import date


class Contacts(NamedTuple):
    email: str
    phone: str
    github: str
    gitlab: str
    skype: str


class EducationLevel(Enum):
    # TODO
    TODO = auto()


class DateInterval(NamedTuple):
    date_from: date
    date_to: date


class EducationPlace(NamedTuple):
    place: str
    speciality: str
    level: EducationLevel
    then: DateInterval


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
    education: List[EducationPlace]
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
    ),
    education=[],
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
