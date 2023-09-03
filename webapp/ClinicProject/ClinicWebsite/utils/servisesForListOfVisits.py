from datetime import datetime, date
from ..models import *
from dataclasses import dataclass
from typing import Generator
from typing import Iterable
from calendar import monthrange, weekday
from django.db import connection


@dataclass
class ListOfVisitsEntity:
    pk: int
    dateOfVisit: datetime
    confirmationOfVisit: bool
    client: int
    employee: int
    get_url_for_watchVisit: str
    
    
@dataclass
class ListOfVisitsEntityWithNames:
    pk: int
    dateOfVisit: datetime
    confirmationOfVisit: bool
    client: str
    employee: str
    # get_url_for_watchVisit: str


class doSomeThingWithListOfVisits:
    __month: int
    __cur_month: int
    __year: int
    __cur_year: int
    __cur_day: int

    __firstWeek: [int]
    __secondWeek: [int]
    __thirdWeek: [int]
    __fourthWeek: [int]
    __fifthWeek: [int]
    
    __query_for_list_of_visits = f"""
                        select DISTINCT ClinicWebsite_listofvisits.dateOfVisit, Staff.name,
                        ClinicWebsite_position.position, ClinicWebsite_loadingdoctors.loading_id,
                        Staff.photo, ClinicWebsite_listofvisits.id

                        from ClinicWebsite_listofvisits,
                        ClinicWebsite_position, Staff, ClinicWebsite_loadingdoctors

                        where ClinicWebsite_listofvisits.employee_id=Staff.id and
                        ClinicWebsite_loadingdoctors.employee_id=Staff.id and
                        ClinicWebsite_position.id=Staff.position_id and
                        
                        ClinicWebsite_listofvisits.client_id IS NULL and
                        date(ClinicWebsite_listofvisits.dateOfVisit)=%s and 
                        ClinicWebsite_position.slug = %s and
                        date(ClinicWebsite_loadingdoctors.date) = %s
                        
                        
                        order by ClinicWebsite_listofvisits.dateOfVisit ,ClinicWebsite_loadingdoctors.loading_id
                        """
    
    __query_for_watchVisits = """
    SELECT ClinicWebsite_listofvisits.id, 
    ClinicWebsite_listofvisits.dateOfVisit, 
    ClinicWebsite_listofvisits.confirmationOfVisit,
    ClinicWebsite_client.name client,
    Staff.name employee

    FROM ClinicWebsite_listofvisits, auth_user, Staff, ClinicWebsite_client

    WHERE ClinicWebsite_listofvisits.employee_id = Staff.id AND
    auth_user.id = Staff.user_id AND Staff.user_id = %s AND
    ClinicWebsite_listofvisits.client_id = ClinicWebsite_client.id

    ORDER BY ClinicWebsite_listofvisits.dateOfVisit
    """

    @staticmethod
    def from_orm_to_entity(visit: listOfVisits) -> ListOfVisitsEntity:
        return ListOfVisitsEntity(
            pk=visit.pk,
            dateOfVisit=visit.dateOfVisit,
            confirmationOfVisit=visit.confirmationOfVisit,
            client=visit.client,
            employee=visit.employee,
            get_url_for_watchVisit=visit.get_absolute_url2(listOfVisits.objects.get(pk=visit.pk).employee.user.pk),
        )
        
    @staticmethod
    def from_raw_to_entity2(*args, **kwargs) -> ListOfVisitsEntity:
        return ListOfVisitsEntity(
            pk=args[0][0],
            dateOfVisit=args[0][1],
            confirmationOfVisit=args[0][2],
            client=args[0][3],
            employee=args[0][4],
            # get_url_for_watchVisit=visit.get_absolute_url2(listOfVisits.objects.get(pk=visit.pk).employee.user.pk),s
        )

    def fetch_all_possible_entries(self) -> Iterable[ListOfVisitsEntity]:
        return list(map(self.from_orm_to_entity, listOfVisits.objects.filter(client__isnull=True, )))
    
    def fetch_one_visit(self, visit_id: int) -> ListOfVisitsEntity:
        return self.from_orm_to_entity(listOfVisits.objects.get(pk=visit_id))

    """For watchVisits view"""
    
    def fetch_all_for_staff(self, userId: int) -> ListOfVisitsEntity:
        return list(map(self.from_orm_to_entity, listOfVisits.objects.filter(
                    employee__user=userId, employee__position__isDoctor=True, client__isnull=False
                    ).order_by('dateOfVisit', 'dateOfVisit__time').select_related('employee')))
    
    def fetch_all_for_client(self, userId: int) -> ListOfVisitsEntity:
        return list(map(self.from_orm_to_entity, listOfVisits.objects.filter(
                    client__user=userId, client__isnull=False
                    ).order_by('dateOfVisit').select_related('client')))
    
    def fetch_onlyActive_for_staff(self, userId: int) -> ListOfVisitsEntity:
        return list(map(self.from_orm_to_entity, listOfVisits.objects.filter(
                    employee__user=userId, confirmationOfVisit=None, employee__position__isDoctor=True, client__isnull=False
                    ).order_by('dateOfVisit').select_related('employee')))
    
    def fetch_onlyActive_for_client(self, userId: int) -> ListOfVisitsEntity:
        return list(map(self.from_orm_to_entity, listOfVisits.objects.filter(
                    client__user=userId, confirmationOfVisit=None, client__isnull=False
                    ).order_by('dateOfVisit').select_related('client')))
    
    def get_visits_for_watchVisits(self, userId: int) -> Iterable[ListOfVisitsEntity]:
        return list(map(self.from_raw_to_entity2, self.push_raw_query(userId, sql=self.__query_for_watchVisits)))
    
    """EndFor watchVisits view"""

    @staticmethod
    def push_raw_query(*args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(kwargs.get('sql'), [*args])
            return list(cursor.fetchall())
    
    @classmethod
    def set_current_date(cls) -> None:
        current_datetime = datetime.now()
        cls.__month, cls.__cur_month, cls.__year, \
            cls.__cur_year, cls.__cur_day = \
            current_datetime.month, current_datetime.month, current_datetime.year, \
                current_datetime.year, current_datetime.day

    def how_many_days_in_current_month(self, month: int = None, year: int = None) -> int:
        if month and year is not None:
            return monthrange(year, month)[1]
        
        return monthrange(self.__year, self.__month)[1]
        
         

    def fetch_first_weekday(self, month: int = None, year: int = None) -> int:
        if month and year is not None:
            return datetime(year, month, 1).weekday()

        return datetime(self.__year, self.__month, 1).weekday()

    def fetch_days_in_weeks(self, month: int = None, year: int = None) -> None:
        days = [i + 1 for i in range(self.how_many_days_in_current_month(month, year))]
        # print(days)
        firstweekday = self.fetch_first_weekday(month, year)

        self.__firstWeek = days[:7 - firstweekday]

        self.__secondWeek = days[7 - firstweekday:7 - firstweekday + 7]

        self.__thirdWeek = days[7 - firstweekday + 7:7 - firstweekday + 7 + 7]

        self.__fourthWeek = days[7 - firstweekday + 7 + 7:7 - firstweekday + 7 + 7 + 7]

        self.__fifthWeek = days[7 - firstweekday + 7 + 7 + 7:7 - firstweekday + 7 + 7 + 7 + 7]
        print(self.__fifthWeek)

    @staticmethod
    def fetch_date_for_query(year: int, month: int, day: int) -> date:
        return (datetime(year, month, day)).date()

    def push_query(self, year: int, month: int, day: int, position_slug: str) -> [[]]:
        date = self.fetch_date_for_query(year, month, day)
        with connection.cursor() as cursor:
            cursor.execute(
                self.__query_for_list_of_visits,
                [date, position_slug, date]
            )

            return list(cursor.fetchall())

    def set_str_month(self, month: int = None) -> str:
        if month is None:
            month = self.__month

        if month == 1:
            month_string = 'Январь'
        elif month == 2:
            month_string = 'Февраль'
        elif month == 3:
            month_string = 'Март'
        elif month == 4:
            month_string = 'Апрель'
        elif month == 5:
            month_string = 'Май'
        elif month == 6:
            month_string = 'Июнь'
        elif month == 7:
            month_string = 'Июль'
        elif month == 8:
            month_string = 'Август'
        elif month == 9:
            month_string = 'Сентябрь'
        elif month == 10:
            month_string = 'Октябрь'
        elif month == 11:
            month_string = 'Ноябрь'
        elif month == 12:
            month_string = 'Декабрь'

        return month_string

    def get_months(self, month: int = None) -> tuple:
        if month is None:
            return self.__month, self.__cur_month
        return month, self.__cur_month

    def get_years(self, year: int = None) -> tuple:
        if year is None:
            return self.__year, self.__cur_year
        return year, self.__cur_year

    def get_weeks(self) -> tuple:
        return self.__firstWeek, \
            self.__secondWeek, \
            self.__thirdWeek, \
            self.__fourthWeek, \
            self.__fifthWeek

    def get_day(self):
        return self.__cur_day

    def fetch_result_values_for_context(self, month: int = None, year: int = None):
        return self.set_str_month(month), \
            self.get_years(year), \
            self.get_months(month), \
            self.get_weeks(), \
            self.fetch_first_weekday(month, year), \
            self.get_day(), \
            self.fetch_all_possible_entries()

    @staticmethod
    def change_date(month, year):
        previous_month = month - 1

        if month > 12:
            month, previous_month = 1, 12
            year += 1
        if month < 1:
            month, previous_month = 12, 1
            year -= 1

        return month, year, previous_month

    def execute_all_methods_for_view(self, month: int = None, year: int = None) -> tuple:
        self.set_current_date()
        self.fetch_days_in_weeks(month, year)

        return self.fetch_result_values_for_context(month, year)
