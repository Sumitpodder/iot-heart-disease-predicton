from django.urls import path, include
from . import views
from .views import download_pdf 

urlpatterns = [
    path("", views.signupPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("home/", views.homePage, name="home"),
    path("disease/", views.diseasePage, name="disease"),
    path('logout/',views.logoutPage,name='logout'),
    path("heart/", views.heart_disease_predictPage, name="heart"),
    path("brain/", views.brain_tumor_predictPage, name="brain"),
    path("history/", views.historyPage, name="history"),
    path('delete_records/', views.delete_records, name='delete_records'),

    path('add/',views.add,name="add"),
    path('edit/',views.edit,name="edit"),
    path('update/<str:id>', views.update,name="update"),
    path('delete/<str:id>',views.delete,name="delete"),
    
    path('live-data/', views.live_data_view, name='live-data'),
    # path('medical-data/', views.medical_form_view, name='medical-data'),
    path('report/', views.reportPage, name='report'),
    path('download-pdf/<int:record_id>/', download_pdf, name='download_pdf'),

]

