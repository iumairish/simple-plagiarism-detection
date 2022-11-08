from django.urls import path
from .views import (
  HomeView,
  AssignmentCreateView,
  AssignmentDetailView,
  AssignmentUpdateView,
  AssignmentSubmissionsView,
  AssignmentSubmissionDetailView,
  AssignmentDeclareResult,
  AssignmentSubmitView,
  AssignmentResultView,
  AssignmentSubmitResultView,
  PlagcheckView
)
from django.conf import settings
from django.conf.urls.static import static

app_name = "core"

urlpatterns = [
  path('', HomeView.as_view(), name='home'),
  path('/assignment-create', AssignmentCreateView.as_view(), name='assignment-create'),
  path('/assignment/<int:pk>', AssignmentDetailView.as_view(), name='assignment-view'),
  path('/assignment/<int:pk>/update', AssignmentUpdateView.as_view(), name='assignment-update'),
  path('/assignment/<int:id>/submissions', AssignmentSubmissionsView.as_view(), name='assignment-submissions'),
  path('/assignment/<int:id>/declare', AssignmentDeclareResult, name='assignment-declare-result'),
  path('/assignment/<int:id>/submissions/<int:id2>', AssignmentSubmissionDetailView.as_view(), name='assignment-submission-view'),
  path('/assignment/<int:id>/submit', AssignmentSubmitView.as_view(), name='assignment-submit'),
  path('/assignment/<int:pk>/result-view', AssignmentResultView.as_view(), name='assignment-result-view'),
  path('/assignment/<int:pk>/result-update', AssignmentSubmitResultView.as_view(), name='assignment-result-update'),
  path('/assignment/<int:pk>/check', PlagcheckView, name='assignment-check')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
