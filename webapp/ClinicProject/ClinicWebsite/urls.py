from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', MainMenu, name='home'),
    path('news/<slug:new_slug>/', fetchNew, name='new'),
    path('about/', about, name='about'),

    # path('staff/', AllStaff, name='AllStaff'),
    path('staff/', AllStaffPosition, name='AllStaff'),

    path('employee/<slug:staff_slug>/', fetchStaff, name='fetchEmployee'),

    path('staff/<slug:position_slug>/', fetchPosition, name='position'),

    path('VisitDoctor/', AllPositionForListOfVisits, name='positionForListOfVisits'),

    path('VisitDoctor/<slug:position_slug>/', DecideToHaveVisitDoctor, name='DecideToHaveVisitDoctor'),

    path('VisitDoctor/<slug:position_slug>/<int:month>/<int:year>',
         DecideToHaveVisitDoctorChangeDate, name='DecideToHaveVisitDoctorChangeDate'),

    path('makeVisitDoctor/<int:visit_id>/',
         makeVisitDoctor, name='makeVisitDoctor'),

    # path('register/', RegisterUser.as_view(), name='register'),
    # path('register/', register, name='register'),
    path('register/', userRegister, name='register'),
    path('login/', userLogin, name='login'),
    path('logout/', userLogout, name='logout'),

    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate,
         name='activate'),

    path("sendEmail/", send_email, name='sendEmail'),

    path("password_reset/", my_password_reset_request, name="password_reset"),

    path('password_reset2/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         my_password_reset_request2,
         name='password_reset2'),

    path("testView/", testView, name='testView'),
    path("testView2/", testView2, name='testView2'),


    path('personal_account/<int:userId>', personalAccount, name='personalAccount'),

    path('watchAllVisits/<int:userId>', watchVisits, name='watchVisits'),

    path('dropVisitDoctor/<int:visit_id>', dropVisitDoctor, name='dropVisitDoctor'),

    path('watchVisit/<int:userId>/<int:visit_id>/', watchVisit, name='watchVisit'),

    path('makeVisitDoctorFromPersonalAcc/<int:userId>/', makeVisitDoctorFromPersonalAcc,
         name='makeVisitDoctorFromPersonalAcc'),

    path('makeDiagnose/<int:userId>/<int:visit_id>/', makeDiagnose, name='makeDiagnose'),

    path('dropDiagnose/<int:userId>/<int:visit_id>/<int:diagnose_id>/', dropDiagnose, name='dropDiagnose'),

    path('makeСonfirmationOfVisit/<int:visit_id>/', makeСonfirmationOfVisit, name='makeСonfirmationOfVisit'),

    path('dropСonfirmationOfVisit/<int:visit_id>/', dropСonfirmationOfVisit, name='dropСonfirmationOfVisit')

]
