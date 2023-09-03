from datetime import datetime
from ..models import *
from dataclasses import dataclass
from typing import Generator
from typing import Iterable


@dataclass
class StaffEntity:
    pk: int
    slug: str
    name: str
    DateOfBirth: datetime
    photo: str
    passport: str
    telephone: str
    address: str
    EmploymentDate: datetime
    get_absolute_url: str

    TheLevelOfEducation: str
    EducationalInstitution: str
    YearOfEnding: int
    DiplomaSpecialty: str

    position: int
    user: int
    PlaceOfWork: int


@dataclass
class StaffEntityAndPositions:
    pk: int
    slug: str
    name: str
    DateOfBirth: datetime
    photo: str
    passport: str
    telephone: str
    address: str
    EmploymentDate: datetime

    get_absolute_url: str

    TheLevelOfEducation: str
    EducationalInstitution: str
    YearOfEnding: int
    DiplomaSpecialty: str

    position: int
    user: int

    position_pk: int
    wage: float
    PlaceOfWork: str
    position_str: str
    slug_position: str


class doSomeThingWithStaff:

    @staticmethod
    def from_orm_to_entity(employee: Staff) -> StaffEntity:
        return StaffEntity(
            pk=employee.pk,
            slug=employee.slug,
            name=employee.name,
            DateOfBirth=employee.DateOfBirth,
            photo=employee.photo.url,
            passport=employee.passport,
            telephone=employee.telephone,
            address=employee.address,
            EmploymentDate=employee.EmploymentDate,
            TheLevelOfEducation=employee.TheLevelOfEducation,
            EducationalInstitution=employee.EducationalInstitution,
            YearOfEnding=employee.YearOfEnding,
            DiplomaSpecialty=employee.DiplomaSpecialty,
            position=employee.position,
            user=employee.user,
            get_absolute_url=employee.get_absolute_url(),
            PlaceOfWork=employee.PlaceOfWork,
        )

    @staticmethod
    def from_orm_to_entity_Staff_Positions(employee) -> StaffEntityAndPositions:
        return StaffEntityAndPositions(
            pk=employee.pk,
            slug=employee.slug,
            name=employee.name,
            DateOfBirth=employee.DateOfBirth,
            photo=employee.photo.url,
            passport=employee.passport,
            telephone=employee.telephone,
            address=employee.address,
            EmploymentDate=employee.EmploymentDate,
            TheLevelOfEducation=employee.TheLevelOfEducation,
            EducationalInstitution=employee.EducationalInstitution,
            YearOfEnding=employee.YearOfEnding,
            DiplomaSpecialty=employee.DiplomaSpecialty,
            position=employee.position,
            user=employee.user,
            get_absolute_url=employee.get_absolute_url(),

            position_pk=employee.position.pk,
            wage=employee.position.wage,
            PlaceOfWork=employee.PlaceOfWork,
            position_str=employee.position.position,
            slug_position=employee.position.slug
        )

    def fetch_all_staff(self) -> Iterable[StaffEntity]:
        return list(map(self.from_orm_to_entity, Staff.objects.filter(position__isDoctor=True)))

    def fetch_all_staff_with_their_positions(self) -> Iterable[StaffEntityAndPositions]:
        return list(map(self.from_orm_to_entity_Staff_Positions, Staff.objects.filter(position__isDoctor=True).select_related('position')))

    def fetch_all_staff_with_filter_by_positions(self, position_slug: str) -> Iterable[StaffEntity]:
        return list(map(self.from_orm_to_entity, Staff.objects.filter(position__slug=position_slug, position__isDoctor=True)))

    def fetch_one_employee(self, slug: str) -> StaffEntity:
        return self.from_orm_to_entity(Staff.objects.get(slug=slug, position__isDoctor=True))


