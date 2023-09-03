from datetime import timedelta, timezone
import time
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView
import requests
import json
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import *

from .forms import *
# from .models import *
# from datetime import datetime
from .utils.servisesForNews import *
from .utils.servisesForPositions import *
from .utils.servisesForStaff import *
from .utils.servisesForListOfVisits import *
from .utils.token import account_activation_token

from django.core.mail import EmailMessage, get_connection
from django.conf import settings


def send_email(request):
    if request.method == "POST":
        with get_connection(
                host=settings.EMAIL_HOST,
                port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            subject = request.POST.get("subject")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST.get("email"), ]
            message = request.POST.get("message")
            EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()

    return render(request, 'ClinicWebsite/send.html')


menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'О поликлинике', 'url_name': 'about'},
    # {'title': 'Администрация', 'url_name': 'administration'},
    {'title': 'Персонал', 'url_name': 'AllStaff'},
    # {'title': 'Адреса', 'url_name': 'addresses'},
    # {'title': 'Расписание врачей', 'url_name': 'Schedule of doctors'},
    # {'title': 'Вакансии', 'url_name': 'Jobs'},
    # {'title': 'Вопросы и предложения', 'url_name': 'Questions and suggestions'},

    # {'title': 'Записаться к врачу', 'url_name': 'DecideToHaveVisitDoctor'},
    {'title': 'Записаться к врачу', 'url_name': 'positionForListOfVisits'},
]


def MainMenu(request):
    news = doSomeThingWithNews().fetch_all_news()

    context = {
        'news': news,
        'menu': menu,
        'title': 'Главная',
        'cur_menu': 'Главная',
    }

    return render(request, 'ClinicWebsite/main.html', context)


def fetchNew(request, new_slug):
    # new = get_object_or_404(News, slug=new_slug)
    new = doSomeThingWithNews().fetch_one_new(new_slug)

    context = {
        'new': new,
        'menu': menu,
    }

    return render(request, 'ClinicWebsite/new.html', context)


def about(request):
    context = {
        'menu': menu,
        'title': 'Сведения о медицинской организации',
        'cur_menu': 'О поликлинике',
    }

    return render(request, 'ClinicWebsite/about.html', context)


def AllStaffPosition(request):
    """Выводит всех сотрудников"""

    # staff = doSomeThingWithStaff().fetch_all_staff_with_their_positions()
    staff = doSomeThingWithStaff().fetch_all_staff()

    positions = doSomeThingWithPosition().fetch_all_positions()

    context = {
        'menu': menu,
        'staff': staff,
        'positions': positions,
        'title': 'Наши специалисты',
        'cur_menu': 'Персонал',
    }

    return render(request, 'ClinicWebsite/Staff.html', context)


def fetchStaff(request, staff_slug):
    """Выводит сотрудника по slug"""

    # employee = get_object_or_404(Staff, slug=staff_slug)
    employee = doSomeThingWithStaff().fetch_one_employee(staff_slug)

    positions = doSomeThingWithPosition().fetch_all_positions()

    context = {
        'menu': menu,
        'positions': positions,
        'employee': employee,
        'title': 'Наши специалисты',
        'cur_menu': ' ',
    }

    return render(request, 'ClinicWebsite/employee.html', context)


def fetchPosition(request, position_slug):
    """Сортирует сотрудников по специальности"""

    staff = doSomeThingWithStaff().fetch_all_staff_with_filter_by_positions(position_slug)

    positions = doSomeThingWithPosition().fetch_all_positions()

    context = {
        'menu': menu,
        'staff': staff,
        'positions': positions,
        'title': 'Наши специалисты',
        'cur_menu': ' ',
        'cur_position': position_slug,
    }

    return render(request, 'ClinicWebsite/Staff.html', context)


def AllPositionForListOfVisits(request):
    """Вывод списка специальностей для listOfVisit"""

    if request.GET and request.user.is_authenticated:
        if request.GET.get('client', False) and request.GET.get('employee', False):
            y = datetime.now().isoformat(sep='|')
            y = y.split('|')
            clientCheck(
                clientCheck.objects.aggregate(Max('pk')).get('pk__max') + 1,
                int(request.GET.get('client')),
                y[0],
                y[1][0:5],
                int(request.GET.get('employee'))).save()

    positions = doSomeThingWithPosition().fetch_all_positions()

    context = {
        'menu': menu,
        'positions': positions,
        'title': 'Выберите специализацию врача',
        'cur_menu': 'Записаться к врачу',
    }

    return render(request, 'ClinicWebsite/baseListOfVisits.html', context)


def DecideToHaveVisitDoctor(request, position_slug):
    """Вывод информации возможным записям"""
    DateSortEntries = []

    positions = doSomeThingWithPosition().fetch_all_positions()

    list_of_visits = doSomeThingWithListOfVisits()

    month_string, years, \
        months, weeks, firstweekday, \
        current_day, possibleEntries = \
        list_of_visits.execute_all_methods_for_view()

    if request.GET:
        if request.GET.get('year', False) and \
                request.GET.get('month', False) and \
                request.GET.get('day', False):
            DateSortEntries = list_of_visits.push_query(
                int(request.GET.get('year')),
                int(request.GET.get('month')),
                int(request.GET.get('day')),
                position_slug)

    context = {
        'menu': menu,
        'cur_menu': ' ',
        'possibleEntries': possibleEntries,
        'month_string': month_string,
        'current_datetime': datetime.now(),
        'firstweekday': firstweekday,
        'range': 7 - firstweekday - 1,
        'firstweek': weeks[0],
        'secondweek': weeks[1],
        'thirdweek': weeks[2],
        'fourthdweek': weeks[3],
        'fifthdweek': weeks[4],
        'month': months[0],
        'DateSortEntries': DateSortEntries,
        'positions': positions,
        'cur_position': position_slug,
        'year': years[0],
        'current_day': current_day,
        'cur_month': months[1],
        'cur_year': years[1],
    }

    return render(request, 'ClinicWebsite/possibleEntries.html', context)


def DecideToHaveVisitDoctorChangeDate(request, position_slug, month, year):
    """Вывод информации возможным записям"""
    """
    cur_month - текущий месяц
    cur_year - текущий год
    year - год, который выводится
    month - месяц, который выводится
    """

    DateSortEntries = []

    positions = doSomeThingWithPosition().fetch_all_positions()

    list_of_visits = doSomeThingWithListOfVisits()

    month, year, previous_month = list_of_visits.change_date(month, year)
    print(month, year)
    print(monthrange(year, month)[1])

    month_string, years, \
        months, weeks, firstweekday, \
        current_day, possibleEntries = \
        list_of_visits.execute_all_methods_for_view(month, year)

    if request.GET:

        if request.GET.get('year', False) and \
                request.GET.get('month', False) and \
                request.GET.get('day', False):
            DateSortEntries = list_of_visits.push_query(
                int(request.GET.get('year')),
                int(request.GET.get('month')),
                int(request.GET.get('day')),
                position_slug)

    context = {
        'menu': menu,
        'cur_menu': ' ',
        'possibleEntries': possibleEntries,
        # 'LastEntries': LastEntries,
        'month_string': month_string,
        'current_datetime': datetime.now(),
        'firstweekday': firstweekday,
        'range': 7 - firstweekday - 1,
        'firstweek': weeks[0],
        'secondweek': weeks[1],
        'thirdweek': weeks[2],
        'fourthdweek': weeks[3],
        'fifthdweek': weeks[4],
        # 'current_month': current_datetime.month,
        'month': months[0],
        # 'days': days,
        'previous_month': previous_month,
        'DateSortEntries': DateSortEntries,
        'positions': positions,
        # 'checkFetchPosition': checkFetchPosition,
        'cur_position': position_slug,
        'year': years[0],
        'current_day': current_day,
        'cur_month': months[1],
        'cur_year': years[1],
    }

    return render(request, 'ClinicWebsite/possibleEntries.html', context)


def makeVisitDoctor(request, visit_id):
    urlForAuth = 'http://127.0.0.1:8001/api/token/'
    urlForModel = 'http://127.0.0.1:8001/apifuzzymodelHeight/v2/'

    sqlRequest = f"""
    select experience, COUNT(ClinicWebsite_listofvisits.id) numberОfСlients, 
    ClinicWebsite_position.norma, 
    (ClinicWebsite_schedule.timeTo - ClinicWebsite_schedule.timeFrom) hours, Staff.id

    from ClinicWebsite_listofvisits, Staff, ClinicWebsite_position, ClinicWebsite_schedule

    WHERE Staff.id = ClinicWebsite_listofvisits.employee_id AND
    ClinicWebsite_position.id = Staff.position_id AND
    Staff.id = ClinicWebsite_schedule.staff_id AND
    ClinicWebsite_listofvisits.client_id IS NOT NULL AND

    ClinicWebsite_listofvisits.employee_id = (
    select ClinicWebsite_listofvisits.employee_id 
    from ClinicWebsite_listofvisits
    WHERE ClinicWebsite_listofvisits.id = %s
    ) AND


    ClinicWebsite_schedule.day = %s

    """
    now = datetime.now()

    start_time = (now - timedelta(minutes=5)).time()
    end_time = (now + timedelta(minutes=5)).time()

    if request.method == 'POST':
        if request.user.is_authenticated:

            try:
                x = clientCheck.objects.filter(employee__user=request.user.id).latest('date', 'time')
                client = x.client.id
                x = x.time
            except:
                x = (now + timedelta(minutes=30)).time()
            if (start_time <= x and x <= end_time):

                listOfVisits.objects.filter(
                    pk=visit_id
                ).update(
                    client=client
                )

            else:
                client = Client.objects.values('id').get(user=request.user.id).get('id')
                position = Staff.objects.values('position').get(
                    id=listOfVisits.objects.values('employee').get(id=visit_id).get('employee')).get('position')
                if visitCheck.objects.filter(
                        client=client,
                        position=position
                ).exists():
                    return HttpResponse(
                        f"У вас уже оформлена запись к {Position.objects.values('position').get(id=position).get('position')}у, " '<a href="http://127.0.0.1:8000/">Главная</a>')
                else:
                    listOfVisits.objects.filter(
                        pk=visit_id
                    ).update(
                        client=Client.objects.get(user=request.user.id)
                    )

                    visitCheck(
                        visitCheck.objects.aggregate(Max('pk')).get('pk__max') + 1,
                        client,
                        position).save()

            try:
                date = listOfVisits.objects.get(id=visit_id).dateOfVisit
                weekday = datetime.weekday(date)
                date = date.date()
                print('weekday: ', weekday)
                with connection.cursor() as cursor:
                    cursor.execute(sqlRequest, [visit_id, weekday])
                    result = list(cursor.fetchone())
                    print(result)

                r = requests.post(urlForAuth, json={"username": "root", "password": "root"})
                data = json.loads(r.text)
                refreshToken, accessToken = data.get("refresh"), data.get("access")

                print('access: ', accessToken)
                print(refreshToken)

                response = requests.get(urlForModel,
                                        headers={'Authorization': f'FuzzyModel {accessToken}'},
                                        data={
                                            "experience": result[0],
                                            "numberОfСlients": result[1],
                                            "border1": 0,
                                            "border2": 5,
                                            "border3": 10,
                                            "norma": result[2],
                                            "hours": result[3]
                                        })

                print(response.json().get('answer')[0][1])
                print(date)

                loadingDoctors.objects.filter(date=date, employee=result[4]).update(
                    loading=response.json().get('answer')[0][1])

            except Exception as e:
                print(e)

            return HttpResponse("Запись прошла успешно, " '<a href="http://127.0.0.1:8000/">Главная</a>')

        else:
            return redirect('login', permanent=True)


def register(request):
    if request.method == "POST":
        # form = UserCreationForm(request.POST)
        form = NewUserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

        user = form.save()
        # login(request, user)
        return redirect('home')

    else:
        # form = UserCreationForm()
        form = NewUserForm()

    context = {
        'menu': menu,
        'form': form,
        'user': request.user.id
    }

    return render(request, 'ClinicWebsite/register.html', context)


def userLogin(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home', permanent=True)

                else:
                    return HttpResponse(
                        'Disabled account'
                        '<a href="http://127.0.0.1:8000/">Главная</a>'
                    )

            else:
                return HttpResponse(
                    'Invalid login'
                    '<hr>'
                    '<a href="http://127.0.0.1:8000/">Главная</a>'
                )

    else:
        form = AuthenticationForm()

    context = {
        'menu': menu,
        'form': form,
    }

    return render(request, 'ClinicWebsite/login.html', context)


@login_required
def userLogout(request):
    logout(request)
    return redirect('home', permanent=True)


def userRegister(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации была отправлена на ваш электронный адрес'
            message = render_to_string('ClinicWebsite/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = [form.cleaned_data.get('username'), ]

            with get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                email_from = settings.EMAIL_HOST_USER
                EmailMessage(mail_subject, message, email_from, to_email, connection=connection).send()

            return HttpResponse('Пожалуйста, подтвердите свой адрес электронной почты, чтобы завершить регистрацию')
    else:
        form = NewUserForm()
    return render(request, 'ClinicWebsite/register.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()  # метод вернет текущую активную модель пользователя
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # расшифровывает/декодирует байтоподобный объект s или строку
        # ASCII, закодированный в Base64
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):  # проверяет соответствует ли токен юзеру
        user.is_active = True
        user.save()
        return HttpResponse(
            'Благодарим вас за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись.'
            '<p <a href="http://127.0.0.1:8000/"></a>Главная</p>'
        )
    else:
        return HttpResponse('Ссылка для активации недействительна!')


def my_password_reset_request(request):
    if request.method == 'POST':
        form = PasswordReset(request.POST)
        if form.is_valid():
            user = User.objects.get(username=form.cleaned_data.get('username'))

            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('ClinicWebsite/password/template_for_email_message.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = [form.cleaned_data.get('username'), ]

            with get_connection(
                    host=settings.EMAIL_HOST,
                    port=settings.EMAIL_PORT,
                    username=settings.EMAIL_HOST_USER,
                    password=settings.EMAIL_HOST_PASSWORD,
                    use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                email_from = settings.EMAIL_HOST_USER
                EmailMessage(mail_subject, message, email_from, to_email, connection=connection).send()

            return HttpResponse('Пожалуйста, проверьте свой email')
    else:
        form = PasswordReset()
    return render(request, 'ClinicWebsite/password/my_pass_reset1.html',
                  {'form': form, 'menu': menu, 'cur_menu': ' ', })


def my_password_reset_request2(request, uidb64, token):
    User = get_user_model()  # метод вернет текущую активную модель пользователя
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # расшифровывает/декодирует байтоподобный объект s или строку
        # ASCII, закодированный в Base64
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):  # проверяет соответствует ли токен юзеру
        if request.method == 'POST':
            form = PasswordReset2(request.POST)
            if form.is_valid():
                if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                    user.set_password(form.cleaned_data.get('password1'))
                    user.save()
                    return redirect('login', permanent=True)
                else:
                    return render(request, 'ClinicWebsite/password/my_pass_reset2.html',
                                  {'form': form, 'menu': menu, 'cur_menu': ' ',
                                   'message': 'пароль1 и пароль2 должны совпадать'})
        else:
            form = PasswordReset2()
            return render(request, 'ClinicWebsite/password/my_pass_reset2.html',
                          {'form': form, 'menu': menu, 'cur_menu': ' ', })
    else:
        return HttpResponse('Ссылка недействительна!')


def testView(request):
    user = 'andrewselan2001@gmail.com'
    print(User.objects.get(username=user))

    query_for_watchVisits = """
    SELECT ClinicWebsite_listofvisits.id, 
    ClinicWebsite_listofvisits.dateOfVisit, 
    ClinicWebsite_listofvisits.confirmationOfVisit,
    Staff.name employee,
    ClinicWebsite_client.name client

    FROM ClinicWebsite_listofvisits, auth_user, Staff, ClinicWebsite_client

    WHERE ClinicWebsite_listofvisits.employee_id = Staff.id AND
    auth_user.id = Staff.user_id AND Staff.user_id = %s AND
    ClinicWebsite_listofvisits.client_id = ClinicWebsite_client.id

    ORDER BY ClinicWebsite_listofvisits.dateOfVisit
    """

    # qwe = doSomeThingWithListOfVisits().get_visits_for_watchVisits(16)

    now = datetime.now()

    start_time = (now - timedelta(minutes=5)).time()
    end_time = (now + timedelta(minutes=5)).time()

    x = clientCheck.objects.filter(employee__user=request.user.id).latest('date', 'time')
    print(now.date() == x.date)
    print(x.time)
    print(start_time, end_time)
    print(start_time <= x.time and x.time <= end_time)
    if start_time <= x.time and x.time <= end_time:
        print(True)

    qwe = 'test view'
    return HttpResponse(f'{qwe}')


from .utils.dao.queries.all_query import AllQuery
from .utils.dao.queries.filter_query import FilterQuery

def testView2(request):

    print(AllQuery().all_query(News, 'title', 'text', 'slug', exceptions='photo'))

    print(FilterQuery().filter_query(Position, 'slug', 'position', 'isDoctor', exceptions='photo', isDoctor=False))

    x = News.objects.all()

    # for key, value in dict(x[1]):
    #     print(key, '   ', value)
    return HttpResponse(x)


@login_required
def personalAccount(request, userId):
    check = False

    information = ()

    if Staff.objects.filter(user_id=userId).exists():
        check = True
        information = Staff.objects.get(user_id=userId)
    elif Client.objects.filter(user_id=userId).exists():
        information = Client.objects.get(user_id=userId)

    context = {
        'menu': menu,
        'i': information,
        'cur_menu': ' ',
        'userId': userId,
        'check': check,
    }

    return render(request, 'ClinicWebsite/personalAccount.html', context)


@login_required
def changePersonalData(request, userId):
    # if Staff.objects.filter(user_id=userId).exists():
    #     information = Staff.objects.filter(user_id=userId)
    if Client.objects.filter(user_id=userId).exists():
        information = Client.objects.filter(user_id=userId)
        flag = True
    else:
        flag = False

    context = {
        'menu': menu,
        'information': information,
        'cur_menu': ' ',
        'flag': flag,
    }

    return render(request, 'ClinicWebsite/personalAccount.html', context)


@login_required
def watchVisits(request, userId):
    flag = False
    if Staff.objects.filter(user_id=userId).exists():
        flag = True

    information = ()
    if request.GET:
        if request.GET.get('url') == 'all':

            if Staff.objects.filter(user_id=userId).exists():
                # information = listOfVisits.objects.filter(
                #     employee__user=userId, employee__position__isDoctor=True, client__isnull=False
                #     ).order_by('dateOfVisit', 'dateOfVisit__time').select_related('employee')
                # information = doSomeThingWithListOfVisits().get_visits_for_watchVisits(userId)
                information = doSomeThingWithListOfVisits().fetch_all_for_staff(userId)

            elif Client.objects.filter(user_id=userId).exists():
                # information = listOfVisits.objects.filter(
                #     client__user=userId, client__isnull=False
                #     ).order_by('dateOfVisit').select_related('client')
                # information = doSomeThingWithListOfVisits().get_visits_for_watchVisits(userId)
                information = doSomeThingWithListOfVisits().fetch_all_for_client(userId)


        elif request.GET.get('url') == 'onlyActive':

            if Staff.objects.filter(user_id=userId).exists():
                # information = listOfVisits.objects.filter(
                #     employee__user=userId, confirmationOfVisit=None, employee__position__isDoctor=True, client__isnull=False
                #     ).order_by('dateOfVisit').select_related('employee')
                information = doSomeThingWithListOfVisits().fetch_onlyActive_for_staff(userId)


            elif Client.objects.filter(user_id=userId).exists():
                # information = listOfVisits.objects.filter(
                #     client__user=userId, confirmationOfVisit=None, client__isnull=False
                #     ).order_by('dateOfVisit').select_related('client')
                information = doSomeThingWithListOfVisits().fetch_onlyActive_for_client(userId)

    context = {
        'menu': menu,
        'information': information,
        'cur_menu': ' ',
        'visitMenu': [
            {'title': 'Все', 'url': 'all'},
            {'title': 'Только активные', 'url': 'onlyActive'},

        ],
        'userId': userId,
        'flag': flag,
    }

    return render(request, 'ClinicWebsite/watchVisits.html', context)


@login_required
def dropVisitDoctor(request, visit_id):
    urlForAuth = 'http://127.0.0.1:8001/api/token/'
    urlForModel = 'http://127.0.0.1:8001/apifuzzymodelHeight/v2/'

    sqlRequest = f"""
    select experience, COUNT(ClinicWebsite_listofvisits.id) numberОfСlients, 
    ClinicWebsite_position.norma, 
    (ClinicWebsite_schedule.timeTo - ClinicWebsite_schedule.timeFrom) hours, Staff.id

    from ClinicWebsite_listofvisits, Staff, ClinicWebsite_position, ClinicWebsite_schedule

    WHERE Staff.id = ClinicWebsite_listofvisits.employee_id AND
    ClinicWebsite_position.id = Staff.position_id AND
    Staff.id = ClinicWebsite_schedule.staff_id AND
    ClinicWebsite_listofvisits.client_id IS NOT NULL AND

    ClinicWebsite_listofvisits.employee_id = (
    select ClinicWebsite_listofvisits.employee_id 
    from ClinicWebsite_listofvisits
    WHERE ClinicWebsite_listofvisits.id = %s
    ) AND


    ClinicWebsite_schedule.day = %s
    """
    print(visit_id)
    if request.method == 'POST':
        if request.user.is_authenticated:

            try:
                date = listOfVisits.objects.get(id=visit_id).dateOfVisit
                weekday = datetime.weekday(date)
                date = date.date()
                print(weekday)
                with connection.cursor() as cursor:
                    cursor.execute(sqlRequest, [visit_id, weekday])
                    result = list(cursor.fetchone())
                    print(result)

                r = requests.post(urlForAuth, json={"username": "root", "password": "root"})
                data = json.loads(r.text)
                refreshToken, accessToken = data.get("refresh"), data.get("access")

                print('access: ', accessToken)
                print('refreshToken: ', refreshToken)
                print('result[1]-1: ', result[1] - 1)
                z = result[1] - 1

                if result[1] - 1 < 0:
                    z = 0
                print('z ', z)
                response = requests.get(urlForModel,
                                        headers={'Authorization': f'FuzzyModel {accessToken}'},
                                        data={
                                            "experience": result[0],
                                            "numberОfСlients": z,
                                            "border1": 0,
                                            "border2": 5,
                                            "border3": 10,
                                            "norma": result[2],
                                            "hours": result[3]
                                        })

                print(response.json().get('answer')[0][1])
                print(date)

                loadingDoctors.objects.filter(date=date, employee=result[4]).update(
                    loading=response.json().get('answer')[0][1])

            except Exception as e:
                print(e)

            if Client.objects.filter(user=request.user.id).exists():
                client = Client.objects.values('id').get(user=request.user.id).get('id')
            else:
                client = listOfVisits.objects.get(id=visit_id).client.id

            position = Staff.objects.values('position').get(
                id=listOfVisits.objects.values('employee').get(id=visit_id).get('employee')).get('position')

            listOfVisits.objects.filter(
                pk=visit_id
            ).update(
                client=None
            )

            visitCheck.objects.get(client=client, position=position).delete()

            return HttpResponse("Запись прошла успешно, " '<a href="http://127.0.0.1:8000/">Главная</a>')

        else:
            return redirect('login', permanent=True)


@login_required
def watchVisit(request, userId, visit_id):
    # visit = doSomeThingWithListOfVisits().fetch_one_visit(visit_id=visit_id)
    flag = False
    if Staff.objects.filter(user_id=userId).exists():
        flag = True

    visit = listOfVisits.objects.get(pk=visit_id)
    history = assigned_diagnoses.objects.values('visit__dateOfVisit', 'disease__name', 'comment', 'id').filter(
        visit__client=listOfVisits.objects.values('client').get(pk=visit_id).get('client'),
        visit__employee__position=listOfVisits.objects.values('employee__position').get(pk=visit_id).get(
            'employee__position')).order_by('visit__dateOfVisit')
    print(listOfVisits.objects.values('employee__position').get(pk=visit_id).get('employee__position'))
    context = {
        'menu': menu,
        'cur_menu': ' ',
        'visit': visit,
        'visit_id': visit_id,
        'visitMenu': [
            {'title': 'Все', 'url': 'all'},
            {'title': 'Только активные', 'url': 'onlyActive'},

        ],
        'userId': userId,
        'history': history,
        'positionOfDoctor': listOfVisits.objects.values(
            'employee__position__position'
        ).get(pk=visit_id).get('employee__position__position'),
        'flag': flag,
    }

    return render(request, 'ClinicWebsite/watchVisit.html', context)


@login_required
def makeVisitDoctorFromPersonalAcc(request, userId, ):
    clients = Client.objects.all()
    employee = Staff.objects.get(user=userId)

    context = {
        'menu': menu,
        'cur_menu': ' ',
        'check': check,
        'visitMenu': [
            {'title': 'Все', 'url': 'all'},
            {'title': 'Только активные', 'url': 'onlyActive'},

        ],
        'userId': userId,
        'clients': clients,
        'employee': employee,
    }

    return render(request, 'ClinicWebsite/makeVisitDoctorFromPersonalAcc.html', context)


@login_required
def makeDiagnose(request, userId, visit_id):
    if request.method == "POST" and Staff.objects.filter(user=request.user.id).exists():
        form = makeDiagnoseForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # print(diagnoses.objects.values('id').get(name=form.cleaned_data.get('disease')))
            # print(form.cleaned_data.get('disease'))
            # diagnose = diagnoses.objects.values('id').get(id=form.cleaned_data.get('disease').id).get('id')
            # print(diagnose)
            assigned_diagnoses.objects.create(
                visit=listOfVisits.objects.get(id=visit_id),
                comment=form.cleaned_data.get('comment'),
                disease=form.cleaned_data.get('disease')
            )
            # return redirect(f'http://127.0.0.1:8000/watchVisit/{userId}/{visit_id}/', permanent=True)
            return redirect('watchVisit', userId=userId, visit_id=visit_id, permanent=True)

    else:
        form = makeDiagnoseForm()

    context = {
        'menu': menu,
        'cur_menu': ' ',
        'check': check,
        'visitMenu': [
            {'title': 'Все', 'url': 'all'},
            {'title': 'Только активные', 'url': 'onlyActive'},

        ],
        'userId': request.user.id,
        'form': form,
        'userId': userId,
    }
    return render(request, 'ClinicWebsite/makeDiagnose.html', context)


@login_required
def dropDiagnose(request, userId, visit_id, diagnose_id):
    if request.method == "POST" and Staff.objects.filter(user=request.user.id).exists():
        assigned_diagnoses.objects.get(id=diagnose_id).delete()

        return redirect('watchVisit', userId=userId, visit_id=visit_id, permanent=True)


@login_required
def makeСonfirmationOfVisit(request, visit_id):
    if request.method == "POST" and Staff.objects.filter(user=request.user.id).exists():
        listOfVisits.objects.filter(
            pk=visit_id
        ).update(
            confirmationOfVisit=True
        )
        z = listOfVisits.objects.get(pk=visit_id)
        client = z.client
        position = z.employee.position
        try:
            visitCheck.objects.get(client=client, position=position).delete()
        except:
            pass

        return HttpResponse(
            "Подтверждение записи прошло успешно, " '<a href="http://127.0.0.1:8000/">Главная</a>'
        )


def dropСonfirmationOfVisit(request, visit_id):
    if request.method == "POST" and Staff.objects.filter(user=request.user.id).exists():
        listOfVisits.objects.filter(
            pk=visit_id
        ).update(
            confirmationOfVisit=None
        )

        z = listOfVisits.objects.get(pk=visit_id)
        client = z.client.id
        position = z.employee.position.id
        try:
            visitCheck(
                visitCheck.objects.aggregate(Max('pk')).get('pk__max') + 1,
                client,
                position).save()
        except:
            pass

    return HttpResponse(
        "Отмена прошла успешно, " '<a href="http://127.0.0.1:8000/">Главная</a>'
    )

# class makeVisitDoctorFromPersonalAcc(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse('GET request!')

#     def post(self, request, *args, **kwargs):
#         return HttpResponse('POST request!')
