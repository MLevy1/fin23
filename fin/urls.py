from django.urls import path
from . import views
from .views import HomePageView, SearchResultsView, testform

urlpatterns = [

    path('', views.main, name='main'),
    path('act/<str:a>/', views.accounts, name='accounts'),
    path('cat/', views.categories, name='categories'),
    path('pay/<str:a>/', views.payees, name='payees'),
    path('trans/', views.transactions, name='transactions'),
    path("aact/", views.aact, name="aact"),
    path("apay/", views.apay, name="apay"),
    path("acat/", views.acat, name="acat"),
    path("atran/", views.atran, name="atran"),
    path("tlist/<str:acc>/<str:cat>/<str:pay>/", views.tlist, name="tlist"),
    path("<int:t_id>/", views.tdetail, name="tdetail"),
    path("issues/", views.issues, name="issues"),
    path("aissue/", views.aissue, name="aissue"),
    path("move/", views.move, name="move"),
    path("uact/<act_id>/", views.uact, name="uact"),
    path("ucat/<cat_id>/", views.ucat, name="ucat"),
    path("upay/<pay_id>/", views.upay, name="upay"),
    path("uissue/<issue_id>/", views.uissue, name="uissue"),
    path("utran/<int:t_id>/", views.utran, name="utran"),
    path("search/", SearchResultsView.as_view(), name="results"),
    path("home/", HomePageView.as_view(), name="home"),
    path("budget/", views.budget, name="budget"),
    path("tdf/", views.trans_data, name="tdf"),
    path("rep/", testform.as_view(), name="testform"),
    path("mult/", views.editpayees, name="editpayees"),
    path("merge/", views.merge_payees, name="merge"),
    path('payee/<int:pk>/delete/', views.delete_payee, name='delete_payee'),
    path('payee/<int:pk>/make_inactive/', views.make_inactive, name='make_inactive'),
]
