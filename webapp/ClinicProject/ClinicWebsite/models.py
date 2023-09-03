from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    text = models.TextField(blank=True, verbose_name='Текст')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    photo = models.ImageField(upload_to='NewsPhoto/%Y/%m/%d', verbose_name='Фото', null=True, blank=True)
    # auto_now_add - время устанавливается в момент добавления новой записи
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    # auto_now - время меняется когда происходит изменение в текущей записи
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь', null=True)

    def get_absolute_url(self):
        return reverse('new', kwargs={'new_slug': self.slug})

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'


class Staff(models.Model):
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    name = models.CharField(max_length=100, verbose_name='ФИО', null=False, db_index=True)
    DateOfBirth = models.DateField(verbose_name='Дата рождения', null=False)
    photo = models.ImageField(upload_to='StaffPhoto/%Y/%m/%d', verbose_name='Фото', null=True, blank=True)
    passport = models.CharField(max_length=10, verbose_name='Паспорт', null=False, unique=True)
    telephone = models.CharField(max_length=15, verbose_name='Номер телефона', null=False)
    address = models.TextField(max_length=255, verbose_name='Адрес', null=False)
    EmploymentDate = models.DateField(verbose_name='Дата приема на работу', null=False)

    TheLevelOfEducation = models.CharField(max_length=40, verbose_name='Уровень образования', null=False)
    EducationalInstitution = models.CharField(max_length=255, null=False, verbose_name='Образовательное учреждение')
    YearOfEnding = models.IntegerField()
    DiplomaSpecialty = models.CharField(max_length=200, null=True, blank=True, verbose_name='Специальность по диплому')

    position = models.ForeignKey('Position', on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)

    experience = models.IntegerField(verbose_name='Опыт работы в годах', null=True)
    PlaceOfWork = models.CharField(max_length=255, verbose_name='Место работы', null=False)

    def get_absolute_url(self):
        return reverse('fetchEmployee', kwargs={'staff_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонал'
        db_table = 'Staff'


class loadingDoctors(models.Model):
    employee = models.ForeignKey('Staff', on_delete=models.PROTECT, verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата')
    loading = models.ForeignKey('loadingLevels', on_delete=models.PROTECT, verbose_name='Загрузка')

    class Meta:
        verbose_name = 'Загрузка врачей'
        verbose_name_plural = 'Загрузка врачей'


class loadingLevels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название уровня загрузки')

    class Meta:
        verbose_name = 'Уровни загрузки'
        verbose_name_plural = 'Уровни загрузки'


class Position(models.Model):
    wage = models.FloatField(verbose_name='Заработная плата')
    position = models.CharField(max_length=100, verbose_name='Должность')
    slug = models.SlugField(max_length=255, db_index=True, unique=True, )
    norma = models.IntegerField(verbose_name='Нормальное кол-во пациентов в час', null=True)
    isDoctor = models.BooleanField(verbose_name='Врач', null=True)

    def __str__(self):
        return self.position

    def get_absolute_url(self):
        return reverse('position', kwargs={'position_slug': self.slug})

    def get_absolute_url_for_listOfVisits(self):
        return reverse('DecideToHaveVisitDoctor', kwargs={'position_slug': self.slug})

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='ФИО', null=False)
    address = models.TextField(max_length=255, verbose_name='Адрес', null=False)
    DateOfBirth = models.DateField(verbose_name='Дата рождения', null=False)
    telephone = models.CharField(max_length=15, verbose_name='Номер телефона', null=False)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    gender = models.CharField(max_length=1, verbose_name='Пол', null=False)
    level = models.ForeignKey('Levels', on_delete=models.PROTECT, null=False)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_slug': self.slug})

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name


class clientCheck(models.Model):
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент', blank=True, null=True)
    date = models.DateField(verbose_name='Дата размещения проверки')
    time = models.TimeField()
    employee = models.ForeignKey('Staff', on_delete=models.PROTECT, verbose_name='Сотрудник', blank=True, null=True)


class Levels(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название уровня')
    AmountRequiredToTransfer = models.IntegerField(verbose_name='Сумма необходимая для перехода')
    AmountOfDiscount = models.FloatField(verbose_name='Скидка', )
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    def get_absolute_url(self):
        return reverse('level', kwargs={'level_slug': self.slug})

    class Meta:
        verbose_name = 'Уровни клиента'
        verbose_name_plural = 'Уровни клиента'


class Schedule(models.Model):
    day = models.CharField(max_length=20, verbose_name='День недели', )
    timeFrom = models.CharField(max_length=10, verbose_name='С')
    timeTo = models.CharField(max_length=10, verbose_name='До')
    staff = models.ForeignKey('Staff', on_delete=models.PROTECT, verbose_name='Сотрудник')

    class Meta:
        verbose_name = 'График работы'
        verbose_name_plural = 'График работы'
        ordering = ['day']


class listOfVisits(models.Model):
    dateOfVisit = models.DateTimeField(null=False, verbose_name='Дата посещения', db_index=True)
    confirmationOfVisit = models.BooleanField(verbose_name='Подтверждение записи', blank=True, null=True, db_index=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT, verbose_name='Клиент', blank=True, null=True,
                               db_index=True)
    employee = models.ForeignKey('Staff', on_delete=models.PROTECT, verbose_name='Врач', db_index=True)

    def get_absolute_url2(self, userId):
        return reverse('watchVisit', kwargs={'userId': userId, 'visit_id': self.pk})

    class Meta:
        verbose_name = 'Список посещений'
        verbose_name_plural = 'Список посещений'

    def __str__(self):
        return str(self.dateOfVisit)


class visitCheck(models.Model):
    client = models.ForeignKey('Client', on_delete=models.PROTECT, blank=True, null=True)
    position = models.ForeignKey('Position', on_delete=models.PROTECT, blank=True, null=True)


class assigned_diagnoses(models.Model):
    visit = models.ForeignKey('listOfVisits', on_delete=models.PROTECT, verbose_name='Посещение')
    disease = models.ForeignKey('diagnoses', on_delete=models.PROTECT, verbose_name='Диагноз')
    comment = models.TextField(verbose_name='Комментарий врача')

    class Meta:
        verbose_name = 'Поставленный диагноз'
        verbose_name_plural = 'Поставленный диагнозы'


class diagnoses(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название болезни', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Диагноз'
        verbose_name_plural = 'Диагнозы'


class check(models.Model):
    summ = models.IntegerField(verbose_name='Сумма')
    visit = models.ForeignKey('listOfVisits', on_delete=models.PROTECT, verbose_name='Посещение')
    payment = models.BooleanField(verbose_name='Оплата', default=False, null=True)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'


class listOfService(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название услуги')
    price = models.IntegerField(verbose_name='Стоимость услуги')

    class Meta:
        verbose_name = 'Список услуг'
        verbose_name_plural = 'Список услуг'


class services_rendered(models.Model):
    service = models.ForeignKey('listOfService', on_delete=models.Model, verbose_name='Оказанная услуга')
    visit = models.ForeignKey('listOfVisits', on_delete=models.PROTECT, verbose_name='Посещение')

    class Meta:
        verbose_name = 'Оказанная услуга'
        verbose_name_plural = 'Оказанные услуги'

