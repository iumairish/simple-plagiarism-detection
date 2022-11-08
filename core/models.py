from django.db import models
from authentication.models import User
from datetime import datetime


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    file = models.FileField(upload_to='media')
    marks = models.CharField(max_length=20)
    result = models.BooleanField(default=False)
    exclude_urls = models.TextField(blank=True)
    due_date = models.DateTimeField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self


class Submissions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, null=True)
    file = models.FileField(upload_to='media')
    marks = models.CharField(max_length=10, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    score = models.CharField(max_length=50, blank=True)
    report = models.CharField(max_length=100, blank=True)
    submit_date = models.DateTimeField(max_length=100, default=datetime.now)

    def __str__(self):
        return self
