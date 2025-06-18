from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from job.models import Job, JobApplication
from job.choices import JobStatusChoices, ApplicationStatusChoices
from job.rest.serializers.serializers import (
    JobListSerializer,
    JobDetailSerializer,
    JobCreateSerializer,
    JobApplicationSerializer,
    JobApplicationStatusSerializer,
    RecruiterDashboardSerializer
)
from shared.permissions import (
    IsRecruiterUser,
    IsCandidateUser,
    IsRecruiterOwnerOrReadOnly,
    IsOwnerOrReadOnly
)

class JobViewSet(viewsets.ModelViewSet):

    queryset = Job.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['job_status', 'location', 'job_type', 'experience_level']
    
    def get_serializer_class(self):

        if self.action == 'list':
            return JobListSerializer
        elif self.action == 'create':
            return JobCreateSerializer
        return JobDetailSerializer
        
    def get_permissions(self):

        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsRecruiterUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsRecruiterOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):

        serializer.save(recruiter=self.request.user)
        
    def get_queryset(self):

        queryset = super().get_queryset()
        

        if getattr(self.request.user, 'role', None) == 'CANDIDATE':
            return queryset.filter(
                job_status=JobStatusChoices.PUBLISHED,
                deadline__gt=timezone.now(),
                status='ACTIVE'
            )

        elif getattr(self.request.user, 'role', None) == 'RECRUITER':
            return queryset.filter(
                recruiter=self.request.user,
                status='ACTIVE'
            )
        return queryset.filter(status='ACTIVE')
        
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated, IsCandidateUser]
    )
    def apply(self, request, pk=None):

        job = self.get_object()
        

        if not (job.job_status == JobStatusChoices.PUBLISHED and 
                job.deadline > timezone.now() and
                job.status == 'ACTIVE'):
            return Response(
                {'detail': 'This job is not currently accepting applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = JobApplicationSerializer(
            data={'job': job.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class JobApplicationViewSet(viewsets.ModelViewSet):

    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['application_status', 'job']
    
    def get_serializer_class(self):

        if self.action in ['update', 'partial_update']:
            return JobApplicationStatusSerializer
        return super().get_serializer_class()
        
    def get_permissions(self):

        if self.action == 'create':

            permission_classes = [IsAuthenticated, IsCandidateUser]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsRecruiterOwnerOrReadOnly]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
    def get_queryset(self):

        queryset = super().get_queryset()
        

        if getattr(self.request.user, 'role', None) == 'CANDIDATE':
            return queryset.filter(
                candidate=self.request.user,
                status='ACTIVE'
            )

        elif getattr(self.request.user, 'role', None) == 'RECRUITER':
            return queryset.filter(
                job__recruiter=self.request.user,
                status='ACTIVE'
            )
        return queryset.filter(status='ACTIVE')

class RecruiterDashboardView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated, IsRecruiterUser]
    serializer_class = RecruiterDashboardSerializer
    
    def get_object(self):

        return self.request.user
        
    def retrieve(self, request, *args, **kwargs):

        user = self.get_object()
        
        stats = {
            'total_published_jobs': Job.objects.filter(
                recruiter=user,
                job_status=JobStatusChoices.PUBLISHED,
                status='ACTIVE'
            ).count(),
            'total_closed_jobs': Job.objects.filter(
                recruiter=user,
                job_status=JobStatusChoices.CLOSED,
                status='ACTIVE'
            ).count(),
            'total_candidate_applications': JobApplication.objects.filter(
                job__recruiter=user,
                status='ACTIVE'
            ).count(),
            'total_candidates_hired': JobApplication.objects.filter(
                job__recruiter=user,
                application_status=ApplicationStatusChoices.ACCEPTED,
                status='ACTIVE'
            ).count(),
            'total_candidates_rejected': JobApplication.objects.filter(
                job__recruiter=user,
                application_status=ApplicationStatusChoices.REJECTED,
                status='ACTIVE'
            ).count(),
        }
        
        serializer = self.get_serializer(stats)
        return Response(serializer.data)