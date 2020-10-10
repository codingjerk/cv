from datetime import date, datetime
from enum import Enum, auto
from io import StringIO
from textwrap import dedent
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class Text:
    language_to_string: Dict[str, str]

    def to_string(self, lang: str) -> str:
        return self.language_to_string[lang]

    def __str__(self):
        raise NotImplementedError


def t(**kwargs: str) -> Text:
    return Text(kwargs)


def s(text: str) -> Text:
    return Text({
        "en": text,
        "ru": text,
    })


@dataclass
class Contacts:
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


@dataclass
class Address:
    country: Text
    city: Text


class EducationLevel(Enum):
    TVET = auto()  # Technical and Vocational Education and Training
    BachelorsDegree = auto()
    MastersDegree = auto()


@dataclass
class YearInterval:
    year_from: int
    year_to: int


@dataclass
class EducationPlace:
    place: Text
    speciality: Text
    level: EducationLevel
    then: YearInterval


@dataclass
class Month:
    year: int
    month: int


@dataclass
class MonthInterval:
    month_from: Month
    month_to: Optional[Month]


@dataclass
class WorkingPlace:
    place: Text
    position: Text
    then: MonthInterval
    description: Text
    achivements: List[Text]
    keywords: List[Text]


class LanguageLevel(Enum):
    Beginner = auto()
    Intermediate = auto()
    Advanced = auto()
    Fluent = auto()
    Native = auto()


@dataclass
class Language:
    name: Text
    level: LanguageLevel


class SalaryPeriod(Enum):
    Annual = auto()
    Monthly = auto()


class SalaryUnit(Enum):
    USD = auto()
    RUB = auto()


@dataclass
class Salary:
    period: SalaryPeriod
    unit: SalaryUnit
    amount: int


@dataclass
class Applicant:
    name: Text
    desired_salary: Salary
    birthdate: date
    contacts: Contacts
    address: Address
    education: List[EducationPlace]
    experience: List[WorkingPlace]
    languages: List[Language]
    skills: List[Text]
    hobbies: List[Text]
    wishes: List[Text]

    def age(self, at: date) -> int:
        return years_between(self.birthdate, at)


@dataclass
class Position:
    name: Text
    about: Text
    skills: List[Text]


@dataclass
class Resume:
    applicant: Applicant
    position: Position

    def to_latex(self, lang: str) -> str:
        generator = LatexGenerator(self, lang)
        return generator.generate()


def d(text: str) -> str:
    """ Dedents text and removes unnecessary newlines """

    return dedent(text).strip()


def is_date_before(test_date: date, point_date: date) -> bool:
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


def make_sequence(delimiters: List[str], elements: List[str]) -> str:
    [first_delimiter, *other_delimiters] = delimiters

    first_delimiter_count = len(elements) - len(other_delimiters)
    delimiters = [first_delimiter] * first_delimiter_count + other_delimiters

    return "".join([
        f"{element}{delimiter}"
        for element, delimiter in zip(elements, delimiters)
    ])


class LatexGenerator():
    contacts_header: Text = t(
        en="Contacts",
        ru="Контакты",
    )

    contacts_note: Text = t(
        en="links are clickable",
        ru="ссылки кликабельны",
    )

    about_header: Text = t(
        en="About",
        ru="Обо мне",
    )

    skills_header: Text = t(
        en="Skills",
        ru="Ключевые навыки",
    )

    languages_header: Text = t(
        en="Languages",
        ru="Языки",
    )

    experience_header: Text = t(
        en="Experience",
        ru="Опыт работы",
    )

    education_header: Text = t(
        en="Education",
        ru="Образование",
    )

    achivements_header: Text = t(
        en="Achivements",
        ru="Достижения",
    )

    hobbies_prefix: Text = t(
        en="I love to",
        ru="Я люблю",
    )

    separators = {
        "en": [", ", " and ", "."],
        "ru": [", ", " и ", "."],
    }

    def __init__(self, resume: Resume, lang: str) -> None:
        self.resume = resume
        self.lang = lang
        self.stream = StringIO()

    def write(self, text: str) -> None:
        self.stream.write(text)

    def write_line(self, line: str) -> None:
        self.write(line + "\n")

    def write_latex_header(self) -> None:
        self.write(d(r"""
            \documentclass[11pt, a4paper]{article}
            \usepackage[papersize={8.5in,11in}]{geometry}
            \usepackage[english,russian]{babel}
            \usepackage{hyperref}
            \usepackage{fontspec}
            \setmainfont{CMU Serif}
            \setsansfont{Noto Sans}
            \setmonofont{Noto Sans Mono}
            \defaultfontfeatures{Extension = .otf}
            \usepackage{fontawesome}
            \usepackage[document]{ragged2e}
            \usepackage{tabularx}
            \usepackage{graphicx}
            \usepackage{wrapfig}

            \pagenumbering{gobble}
        """))

    def write_phone(self) -> None:
        self.write_link_with_icon(
            url=f"tel:{self.resume.applicant.contacts.phone}",
            icon="phone",
            text=self.resume.applicant.contacts.beauty_phone(),
        )

    def write_email(self) -> None:
        email = self.resume.applicant.contacts.email
        self.write_link_with_icon(
            url=f"mailto:{email}",
            icon="phone",
            text=email,
        )

    def write_text_with_icon(self, icon: str, text: str) -> None:
        self.write(r"\faicon{%s} & %s" % (icon, text))

    def write_link_with_icon(self, url: str, icon: str, text: str) -> None:
        text_with_url = rf"\href{{{url}}}{{{text}}}"
        self.write_text_with_icon(icon, text_with_url)

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
        username = self.resume.applicant.contacts.linkedin
        self.write_link_with_icon(
            url=f"https://linkedin.com/in/{username}",
            icon="linkedin",
            text=username,
        )

    def write_web(self) -> None:
        site = self.resume.applicant.contacts.web
        self.write_link_with_icon(
            url=f"https://{site}",
            icon="globe",
            text=site,
        )

    def write_address(self) -> None:
        country = self.resume.applicant.address.country.to_string(self.lang)
        city = self.resume.applicant.address.city.to_string(self.lang)

        self.write_text_with_icon(
            icon="map-marker",
            text=rf"{city} ({country})",
        )

    def write_contacts(self) -> None:
        contacts_header = self.contacts_header.to_string(self.lang)
        contacts_note = self.contacts_note.to_string(self.lang)
        self.write_line(f"\\textbf{{\Large {contacts_header}}} \\footnotesize{{\\normalfont ({contacts_note})}}")
        self.write_line(r"\vspace{0.75em}")
        self.write_line(r"\hrule")
        self.write_line(r"\leftskip0.7cm\relax")
        self.write_line(r"\vspace{1em}")
        self.write_line(r"\begin{tabular}{ c l c l c l }")

        self.write_address()
        self.write_line("&")
        self.write_github()
        self.write_line("&")
        self.write_linkedin()
        self.write_line(r"\\")

        self.write_phone()
        self.write_line("&")
        self.write_gitlab()
        self.write_line("&")
        self.write_skype()
        self.write_line(r"\\")

        self.write_email()
        self.write_line("&")
        self.write_web()

        self.write_line(r"\end{tabular}")
        self.write_line("")
        self.write_line(r"\leftskip0cm\relax")
        self.write_line(r"\vspace{1.5em}")

    def write_photo(self) -> None:
        self.write_line(r"""
            \begin{wrapfigure}[2]{r}{8em}
                \vspace{-1.75em}
                \includegraphics[width=6em]{photo.png}
            \end{wrapfigure}
        """)

    def write_name(self) -> None:
        name = self.resume.applicant.name.to_string(self.lang)
        self.write_line(rf"\textbf{{\huge {name}}}")
        self.write_line(r"\vspace{1em}")
        self.write_line("")

    def write_position(self) -> None:
        position = self.resume.position.name.to_string(self.lang)
        self.write_line(rf"\textbf{{\LARGE {position}}}")
        self.write_line(r"\vspace{1em}")
        self.write_line("")

    def write_age(self) -> None:
        the_moment = datetime.now()
        age = self.resume.applicant.age(at=the_moment)

        self.write_line(rf"{age} years old")

    def write_header(self) -> None:
        self.write_photo()
        self.write_name()
        self.write_position()
        self.write_line(r"\vspace{2em}")

        self.write_contacts()

    def write_skill(self, skill: str) -> None:
        self.write_line(fr"\item {skill}")

    def write_all_skills(self) -> None:
        skills_header = self.skills_header.to_string(self.lang)
        self.write_line(f"\\textbf{{\\Large {skills_header}}}")
        self.write_line(r"\vspace{0.75em}")
        self.write_line(r"\hrule")
        self.write_line(r"\vspace{1em}")

        self.write_line(r"\begin{itemize}")
        self.write_line(r"\setlength\itemsep{0em}")
        self.write_line(r"\rightskip2.5cm\relax")

        skills = make_sequence(
            self.separators[self.lang],
            [
                skill.to_string(self.lang)
                for skill in self.resume.applicant.skills
            ],
        )
        self.write_line(fr"\item[] Soft: {skills}")

        skills = make_sequence(
            self.separators[self.lang],
            [
                skill.to_string(self.lang)
                for skill in self.resume.position.skills
            ],
        )
        self.write_line(fr"\item[] Hard: {skills}")

        self.write_line(r"\end{itemize}")
        self.write_line(r"\vspace{1.5em}")

    def write_language(self, language: Language) -> None:
        name = language.name.to_string(self.lang)
        level = {
            (LanguageLevel.Intermediate, "en"): "Intermediate",
            (LanguageLevel.Advanced, "en"): "Advanced",
            (LanguageLevel.Fluent, "en"): "Fluent",
            (LanguageLevel.Native, "en"): "Native",

            (LanguageLevel.Intermediate, "ru"): "Средний",
            (LanguageLevel.Advanced, "ru"): "Продвинутый",
            (LanguageLevel.Fluent, "ru"): "Беглый",
            (LanguageLevel.Native, "ru"): "Родной",
        }[(language.level, self.lang)]

        self.write_line(fr"\item[] {name} ({level})")

    def write_all_languages(self) -> None:
        languages_header = self.languages_header.to_string(self.lang)
        self.write_line(f"\\textbf{{\\Large {languages_header}}}")
        self.write_line(r"\vspace{0.75em}")
        self.write_line(r"\hrule")
        self.write_line(r"\vspace{1em}")

        self.write_line(r"\begin{itemize}")
        self.write_line(r"\rightskip2.5cm\relax")
        self.write_line(r"\setlength\itemsep{0em}")

        for language in self.resume.applicant.languages:
            if language.level == LanguageLevel.Beginner:
                continue

            self.write_language(language)

        self.write_line(r"\end{itemize}")
        self.write_line(r"\vspace{1.5em}")

    def write_working_place(self, working_place: WorkingPlace, first: bool) -> None:
        if not first:
            self.write_line(r"\vspace{1em}")

        self.write_line(fr"""
            \item[]
            \textbf{{\large {working_place.position.to_string(self.lang)}}}

            \textbf{{{working_place.place.to_string(self.lang)}}}
        """)

        self.write_line(working_place.description.to_string(self.lang))
        self.write_line("")

        achivements_header = self.achivements_header.to_string(self.lang)
        self.write_line(rf"\textbf{{{achivements_header}}}")
        self.write_line(r"\begin{itemize}")
        self.write_line(r"\rightskip2.5cm\relax")
        self.write_line(r"\setlength\itemsep{0em}")
        for achivement in working_place.achivements:
            self.write_line(rf"\item[$\bullet$] {achivement.to_string(self.lang)}")
        self.write_line(r"\end{itemize}")

    def write_all_working_places(self) -> None:
        experience_header = self.experience_header.to_string(self.lang)
        self.write_line(f"\\textbf{{\\Large {experience_header}}}")
        self.write_line(r"\vspace{0.75em}")
        self.write_line(r"\hrule")
        self.write_line(r"\vspace{1em}")

        self.write_line(r"\begin{itemize}")
        self.write_line(r"\rightskip2.5cm\relax")
        self.write_line(r"\setlength\itemsep{0em}")

        experience = enumerate(reversed(self.resume.applicant.experience))
        for index, working_place in experience:
            self.write_working_place(working_place, first=(index == 0))

        self.write_line(r"\end{itemize}")
        self.write_line(r"\vspace{1.5em}")

    def write_education_place(self, education_place: EducationPlace, first: bool) -> None:
        level = {
            (EducationLevel.TVET, "en"): "TVET",
            (EducationLevel.BachelorsDegree, "en"): "Bachelor's degree",
            (EducationLevel.MastersDegree, "en"): "Master's degree",

            (EducationLevel.TVET, "ru"): "Среднее профессиональное",
            (EducationLevel.BachelorsDegree, "ru"): "Бакалавр",
            (EducationLevel.MastersDegree, "ru"): "Магистр",
        }[(education_place.level, self.lang)]

        if not first:
            self.write_line(r"\\")

        self.write_line(fr"""
            {education_place.then.year_to} &
            \textbf{{\large{{{education_place.place.to_string(self.lang)}}}}} &
            {level}
            \\
            & {education_place.speciality.to_string(self.lang)}
            \\
        """)

    def write_all_education_places(self) -> None:
        education_header = self.education_header.to_string(self.lang)
        self.write_line(f"\\textbf{{\\Large {education_header}}}")
        self.write_line(r"\vspace{0.75em}")
        self.write_line(r"\hrule")
        self.write_line(r"\vspace{1em}")

        self.write_line(r"\leftskip0.7cm\relax")
        self.write_line(r"\begin{tabularx}{42em}{ r X r }")

        education = enumerate(reversed(self.resume.applicant.education))
        for index, education_place in education:
            self.write_education_place(education_place, first=(index == 0))

        self.write_line(r"\end{tabularx}")
        self.write_line(r"\vspace{1.5em}")

    def write_about(self) -> None:
        loves = make_sequence(
            self.separators[self.lang],
            [
                hobbie.to_string(self.lang)
                for hobbie in self.resume.applicant.hobbies
            ],
        )

        about_header = self.about_header.to_string(self.lang)
        hobbies_prefix = self.hobbies_prefix.to_string(self.lang)
        self.write_line(f"\\textbf{{\\Large {about_header}}}")
        self.write_line(r"\vspace{0.75em}")
        self.write_line(r"\hrule")
        self.write_line(r"\vspace{1em}")
        self.write_line(rf"""{{
            \leftskip0.95cm\relax
            \rightskip2.5cm\relax
            {self.resume.position.about.to_string(self.lang)}

            {hobbies_prefix} {loves}

        }}""")
        self.write_line(r"\vspace{1.5em}")


    def write_content(self) -> None:
        self.write_header()
        self.write_about()
        self.write_all_skills()
        self.write_all_languages()
        self.write_all_working_places()
        self.write_all_education_places()

    def write_document(self) -> None:
        self.write_line(r"\begin{document}")
        self.write_content()
        self.write_line(r"\end{document}")

    def generate(self) -> str:
        self.write_latex_header()
        self.write_document()

        return self.stream.getvalue()


me = Applicant(
    name=t(
        en="Denis Gruzdev",
        ru="Груздев Денис",
    ),
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
        country=t(
            en="Russia",
            ru="Россия",
        ),
        city=t(
            en="Moscow",
            ru="Москва",
        ),
    ),
    education=[
        EducationPlace(
            place=t(
                en="Moscow College of Railway Transport",
                ru="Московский колледж железножорожного транспорта",
            ),
            speciality=t(
                en="Automatic Information Processing and Control Systems",
                ru="Автоматизированные системы обработки информации и управления",
            ),
            level=EducationLevel.TVET,
            then=YearInterval(2011, 2014),
        ),
        EducationPlace(
            place=t(
                en="Moscow Power Engineering Institute",
                ru="Московский энергетический институт",
            ),
            speciality=t(
                en="Computer Science and Engineering",
                ru="Информатика и вычислительная техника",
            ),
            level=EducationLevel.BachelorsDegree,
            then=YearInterval(2014, 2017),
        ),
        EducationPlace(
            place=t(
                en="Moscow Power Engineering Institute",
                ru="Московский энергетический институт",
            ),
            speciality=t(
                en="Applied Mathematics and Informatics",
                ru="Прикладная математика и информатика",
            ),
            level=EducationLevel.MastersDegree,
            then=YearInterval(2020, 2022),
        ),
    ],
    experience=[
        WorkingPlace(
            place=t(
                en="Navigator Bank",
                ru="Навигатор Банк",
            ),
            position=t(
                en="Junior Software Developer",
                ru="Младший разработчик",
            ),
            then=MonthInterval(Month(2010, 7), Month(2012, 12)),
            description=t(
                en=d("""
                    I started working here half-time, just after I graduated from a highschool.
                    We worked on accounting system for money transfers (Unistream, CONTACT, Western Union, KoronaPay) using Delphi and C++ as our primary programming languages paired with FoxPro database.
                    Even on half-time job I've learned a lot.
                """),
                ru=d("""
                    Я начал работать на полставки сразу после окончания школы, я занимался поддержкой системы учета для денежных переводов, использовал Delphi и C++ как основные языки в паре с БД FoxPro.
                    Даже работая на полставки я многому научился.
                """),
            ),
            achivements=[
                t(
                    en="Improved performance of legacy report generation system",
                    ru="Улучшил производительность системы генерации отчетов",
                ),
                t(
                    en="Extended accounting system with client database module",
                    ru="Расширил систему учета модулем с базой клиентов",
                ),
                t(
                    en="Added autocompletion feature to input forms",
                    ru="Добавил автодополнение в формы ввода",
                ),
            ],
            keywords=[
                s("Delphi"),
                s("C++"),
                s("FoxPro"),
            ],
        ),
        WorkingPlace(
            place=t(
                en="Central Scientific Research Institute of Chemistry and Mechanics",
                ru="Центральный научно-исследовательский институт химии и механики",
            ),
            position=t(
                en="Software Developer (Computer Vision)",
                ru="Разработчик CV",
            ),
            then=MonthInterval(Month(2014, 6), Month(2015, 4)),
            description=t(
                en=d("""
                    It was a very interesting job with embedded devices, computer vision and a lot of creativity.
                    I've worked on classified goverment projects, so I can't tell the details.
                """),
                ru=d("""
                    Это была очень интересная работа со встраиваемыми устройствами, компьютерным зрением и возможностью поработать с кучей железок.
                    Подробная информация о проектах является гостайной, поэтому я не могу рассказать детали.
                """),
            ),
            achivements=[
                t(
                    en="Developed a video translation module for computer vision system of unmanned aerial vehicle",
                    ru="Разработал модуль видеотранстялции для системы компьютерного зрения беспилотного аппарата",
                ),
                t(
                    en="Created a tool to monitor and control our embedded devices",
                    ru="Создал средство мониторинга и управления нашими встраиваемыми устройствами",
                ),
                t(
                    en="Created it's mobile version with C++ and Android NDK",
                    ru="Написал его мобильную версию с C++ и Android NDK",
                ),
                t(
                    en="Trained a junior developer and taught him basics of computer vision",
                    ru="Обучил младшего разработчика, дав ему основы разработки и компьютерного зрения",
                ),
            ],
            keywords=[
                s("C/C++"),
                s("Python"),

                s("Qt"),
                s("OpenCV"),
                s("Embedded Programming"),
                s("Android NDK"),

                s("Computer Vision"),
            ],
        ),
        WorkingPlace(
            place=s("Paragon Software"),
            position=t(
                en="Python/C++ Developer",
                ru="Python/C++ разработчик",
            ),
            then=MonthInterval(Month(2015, 4), Month(2016, 10)),
            description=t(
                en=d("""
                    We have been creating educational software, such as interactive schoolbooks and interactive learning boards for Mathematics, Physics, Geographics, etc.
                """),
                ru=d("""
                    Мы создавали образовательное ПО, такое как интерактивные учебники и интерактивные доски для преподавания математики, физики, географии и других предметов.
                """),
            ),
            achivements=[
                t(
                    en="Writed an integration system to convert existing e-books to our format, which allowed us to increase typists productivity",
                    ru="Реализовал автоматизированное конвертирование существующих электронных учебников в наш внутренний формат, что позволило улучшить производительность верстальщиков",
                ),
                t(
                    en="Created an internal package manager from scratch",
                    ru="Создал пакетный менеджер для внутреннего использования",
                ),
                t(
                    en="Increased code coverage to about 100\% in all projects",
                    ru="Увеличил покрытие кода до приблизительно 100\% во всех проектах",
                ),
                t(
                    en="Mentored trainees and taught them until they became our junior developers",
                    ru="Наставлял стажеров и обучал их до тех пор, пока они не присоединились к нашей команде в качестве младших разработчиков",
                ),
            ],
            keywords=[
                s("C++"),
                s("Python"),
                s("JavaScript/CoffeeScript"),
                s("Node.js"),

                s("wxWidgets"),
                s("Box2D"),
                s("XPath"),
                s("Selenium"),
                s("Electron"),

                s("Data Mining"),
            ],
        ),
        WorkingPlace(
            place=s("Фриланс"),
            position=s("Фуллстек разработчик"),
            then=MonthInterval(Month(2017, 1), Month(2019, 4)),
            description=s(d("""
                I worked with customers from different countries on international freelance platform.
                In the main I've accepted small tasks related to web, automation or data mining.
                As a result in additional to getting a lot of skills I've learned time management and improved my communication skills.
            """)),
            achivements=[
                s("Created queue-based image processing system for DeepDream iOS application"),
                s("Fixed minor issues in 30+ web sites"),
                s("Wrote data mining tools and web scrappers for 20+ sources"),
            ],
            keywords=[
                s("Python"),
                s("JavaScript/TypeScript"),
                s("Bash"),

                s("React.js"),
                s("Flask/Bottle"),

                s("Redis"),
                s("PostgreSQL"),
                s("MongoDB"),

                s("Kafka"),
                s("RabbitMQ"),

                s("Web Development"),
                s("Automation"),
                s("Data Mining"),
            ],
        ),
        WorkingPlace(
            place=s("Polymedia"),
            position=t(
                en="Web/ETL Developer",
                ru="Python разработчик",
            ),
            then=MonthInterval(Month(2019, 4), None),
            description=t(
                en=d("""
                    We created a buisness intelligence platform Visiology, integrated it with various data sources and customized it to customer needs.
                    I've learned a lot about databases, OLAP-cubes. Learned how to improve uncultivated development process and how to lead small teams.
                """),
                ru=d("""
                    Мы создавали BI-платформу Visiology, интегрировали её с различными источниками данных и кастомизировали под нужды заказчиков.
                    Я узнал многое о базах данных, в том числе многомерных. Удалось научиться улучению неразвитого процесса разработки и управлению маленькими командами.
                """),
            ),
            achivements=[
                t(
                    en="Improved development process and overall products quality by introducing gitflow, continous integration, style guides, code reviews, unit and smoke testing",
                    ru="Улучшил процесс разработки введением gitflow, CI, стайлгайдов, код-ревью, модульного и смоук тестирования",
                ),
                t(
                    en="Improved performance of XML parsing by creating specialized XML parser as Python Extension Module with Rust",
                    ru="Увелиличил производительность парсинга XML созданием специализированного парсера для Python на Rust",
                ),
                t(
                    en="Improved maintainability of several legacy projects by rewriting from scratch and/or gradual refactoring",
                    ru="Улучшил качество нескольких легаси проектов переписав их с нуля или постепенным рефакторингом",
                ),
                t(
                    en="Created several forecasting models using machine learning",
                    ru="Создал несколько прогнозных моделей с применением машинного обучения",
                ),
                t(
                    en="Mentored and trained a lot of junior Python and JavaScript developers and new employees",
                    ru="Наставлял и обучал младших разработчиков и новых работников",
                ),
                t(
                    en="Led a team of four developers for half a month",
                    ru="Управлял командой из четырёх разработчиков пол месяца",
                ),
            ],
            keywords=[
                s("Python"),
                s("SQL"),
                s("JavaScript"),

                s("Data Warehouse"),
                s("OLAP"),

                s("Buisness Intelligence"),
                s("Web Development"),
                s("ETL"),
            ],
        ),
    ],
    languages=[
        Language(
            t(
                en="Russian",
                ru="Русский",
            ),
            LanguageLevel.Native,
        ),
        Language(
            t(
                en="English",
                ru="Английский",
            ),
            LanguageLevel.Intermediate,
        ),
        Language(
            t(
                en="French",
                ru="Французский",
            ),
            LanguageLevel.Beginner,
        ),
        Language(
            t(
                en="Esperanto",
                ru="Эсперанто",
            ),
            LanguageLevel.Beginner,
        ),
    ],
    skills=[
        t(
            en="time management (work-load handling, scheduling)",
            ru="тайм-менеджмент",
        ),
        t(
            en="training/mentoring junior developers",
            ru="обучение/менторство",
        ),
        t(
            en="gradual improvement of legacy code",
            ru="последовательное улучшение легаси-кода",
        ),
    ],
    hobbies=[
        t(
            en="learning romance languages",
            ru="изучать романские языки",
        ),
        t(
            en="drawing hands with pen",
            ru="рисовать руки",
        ),
        t(
            en="playing guitar",
            ru="играть на гитаре",
        ),
        t(
            en="reading tech books",
            ru="читать техническую литературу",
        ),
        t(
            en="using Haskell and Rust in pet-projects",
            ru="использовать Haskell и Rust в пет-проектах",
        ),
        t(
            en="writing compilers",
            ru="писать компиляторы",
        ),
    ],
    wishes=[
        t(
            en="Learning new domains",
            ru="Изучать новые предметные области",
        ),
        t(
            en="Working with awesome people",
            ru="Работать в крутой команде",
        ),
        t(
            en="Creating awesome product",
            ru="Создавать крутой продукт",
        ),
    ],
)


python_developer = Position(
    name=t(
        en="Python Developer",
        ru="Разработчик Python",
    ),
    about=t(
        en=d("""
            I have over 6 years of experience as a software engineer and have worked at both small and large organizations.
            I'm mostly Backend/ETL developer with knowledge of Python, JavaScript and some SQL and C++.
        """),
        ru=d("""
            У меня более 6 лет опыта разработки програмного обеспечения, я работал как в маленьких так и в больших командах.
            В основном я занимаюсь разработкой бекенда и ETL с использованием Python, а также знаю JavaScript и немного SQL и C++.
        """),
    ),
    skills=[
        s("python"),
        s("mypy/typing"),
        s("REST/RESUful API"),
        s("postgreSQL"),
        s("linux"),
        s("docker"),
        s("git"),
        s("automated testing"),
        s("continious integration"),
    ],
)


if __name__ == "__main__":
    latex = Resume(me, python_developer).to_latex(lang="ru")
    print(latex)
