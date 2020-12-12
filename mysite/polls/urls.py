from django.urls import path
from . import views

app_name="polls"

urlpatterns=[

    

    path('quiz/',views.quiz,name='quiz'),
    path('<int:quiz_id>/list/', views.polls_list, name='list'),
    path('<int:poll_id>/detail/', views.poll_detail , name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
    path('resultsdata/<int:poll_id>/',views.resultsData,name='resultsdata'),

]