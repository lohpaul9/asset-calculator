from django.urls import path, include
from . import views
from rest_framework.authtoken import views as authtokenviews

urlpatterns = [
    path('stocktrxns/', views.StockTrxnList.as_view()),
    path('stocktrxns/<int:pk>/', views.StockTrxnDetail.as_view()),
    path('cashentries/', views.CashEntryList.as_view()),
    path('cashentries/<int:pk>/', views.CashEntryDetail.as_view()),
    path('acrosstime/', views.AnalysisAcrossTime.as_view()),
    path('', views.FullUserDetail.as_view()),
    # path('login/', include('rest_framework.urls')),
    path('login/', authtokenviews.obtain_auth_token),
    path('signup/', views.UserSignUp.as_view())
]
