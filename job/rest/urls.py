from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job.rest.views.views import (
    JobViewSet,
    JobApplicationViewSet,
    RecruiterDashboardView
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', JobApplicationViewSet, basename='application')

urlpatterns =[
    
    path('recruiter-dashboard/', RecruiterDashboardView.as_view(), name='recruiter-dashboard'),
]
urlpatterns += router.urls  