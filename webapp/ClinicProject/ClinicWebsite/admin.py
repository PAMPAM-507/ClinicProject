from django.contrib import admin
from .models import *


# admin.site.register(News)
# admin.site.register(Staff)

# admin.site.register(Client)
# admin.site.register(Position)
# admin.site.register(listOfVisits)

# admin.site.register(assigned_diagnoses)
# admin.site.register(diagnoses)
# admin.site.register(Schedule)
# admin.site.register(loadingDoctors)
# admin.site.register(loadingLevels)

@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('id', 'title', 'text', 'slug', 'get_photo',
                    'time_create', 'time_update', 'is_published', 'user')
    list_display_links = ('id', 'title',)
    search_fields = ('id', 'title', 'slug',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} width="50", height="60"')

    get_photo.short_description = 'Фото'


@admin.register(Staff)
class AdminStaff(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'user', 'get_photo',
                    'telephone', 'EmploymentDate', 'get_position', 'PlaceOfWork')
    list_display_links = ('id', 'slug', 'name', 'user',)
    search_fields = ('id', 'slug', 'name', 'user',)
    list_filter = ('position__position',)
    fields = (
        'slug', 'name', 'get_photo', 'photo', 'DateOfBirth', 'passport',
        'telephone', 'address', 'EmploymentDate', 'TheLevelOfEducation',
        'EducationalInstitution', 'YearOfEnding', 'DiplomaSpecialty',
        'position', 'user', 'experience', 'PlaceOfWork',)
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} width="150", height="150"')

    get_photo.short_description = 'Фото'

    def get_position(self, obj):
        return mark_safe(f'{obj.position.position}')


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'user', 'address',
                    'DateOfBirth', 'telephone', 'gender',)
    list_display_links = ('id', 'slug', 'name', 'user',)
    search_fields = ('id', 'slug', 'name', 'user', 'address',
                     'telephone', 'gender',)
    list_filter = ('gender',)


@admin.register(Position)
class AdminPosition(admin.ModelAdmin):
    list_display = ('id', 'position', 'slug', 'wage', 'norma', 'isDoctor')
    list_display_links = ('id', 'slug', 'position',)
    search_fields = ('id', 'wage', 'slug', 'name', 'position', 'isDoctor', 'norma')
    list_editable = ('isDoctor',)
    list_filter = ('position', 'isDoctor',)


@admin.register(Schedule)
class AdminSchedule(admin.ModelAdmin):
    list_display = ('id', 'day', 'staff', 'get_position', 'timeFrom', 'timeTo',)
    list_display_links = ('id', 'day', 'staff',)
    search_fields = ('id', 'day', 'timeFrom', 'timeTo', 'staff',)
    list_filter = ('day', 'staff__position__position', 'staff',)

    def get_staff_id(self, obj):
        return mark_safe(f'{obj.staff.id}')

    def get_position(self, obj):
        return mark_safe(f'{obj.staff.position.position}')


@admin.register(listOfVisits)
class AdminListOfVisits(admin.ModelAdmin):
    list_display = ('id', 'dateOfVisit', 'client', 'employee',
                    'get_photo', 'confirmationOfVisit',)
    list_display_links = ('id', 'dateOfVisit', 'client', 'employee',)
    search_fields = ('id', 'dateOfVisit', 'client', 'employee', 'confirmationOfVisit',)
    list_editable = ('confirmationOfVisit',)
    list_filter = ('confirmationOfVisit', 'employee__position__position',)
    fields = ('dateOfVisit', 'client', 'employee', 'get_photo',
              'confirmationOfVisit',)
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.employee.photo:
            return mark_safe(f'<img src={obj.employee.photo.url} width="100", height="100"')

    get_photo.short_description = 'Фото врача'


@admin.register(assigned_diagnoses)
class AdminAssigned_diagnoses(admin.ModelAdmin):
    list_display = ('id', 'visit', 'disease', 'comment',)
    list_display_links = ('id', 'visit',)
    search_fields = ('id', 'visit', 'disease', 'comment',)
    list_filter = ('disease',)


@admin.register(diagnoses)
class AdminDiagnoses(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)


@admin.register(loadingDoctors)
class AdminLoadingDoctors(admin.ModelAdmin):
    list_display = ('date', 'employee', 'get_name_of_load',)
    list_display_links = ('employee', 'date', 'get_name_of_load',)
    search_fields = ('employee', 'date', 'get_name_of_load',)
    list_filter = ('loading__name', 'employee',)

    def get_name_of_load(self, obj):
        return mark_safe(f'{obj.loading.name}')


@admin.register(loadingLevels)
class AdminLoadingLevels(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    list_filter = ('id', 'name',)

    # list_display =
    # list_display_links =
    # search_fields =
    # list_editable =
    # list_filter =
    # fields =
    # readonly_fields =
# admin.site.register(check)
# admin.site.register(listOfService)
# admin.site.register(services_rendered)
# admin.site.register(Levels)