from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# Choices for various fields
BRANCH_CHOICES = [
    ('Computer Science', 'Computer Science'),
    ('Mechanical', 'Mechanical'),
    ('Civil', 'Civil'),
    ('Electronics', 'Electronics'),
    ('Electric', 'Electric'),
    ('IT', 'Information Technology'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('Accept', 'Accepted'),
    ('Reject', 'Rejected'),
]

CATEGORY_CHOICES = [
    ('Notes', 'Notes'),
    ('ModelPapers', 'Model Papers'),
    ('Guidance', 'Career Guidance'),
]

FILE_TYPE_CHOICES = [
    ('PDF', 'PDF'),
    ('PPT', 'PowerPoint'),
    ('DOC', 'Word Document'),
    ('TXT', 'Text File'),
    ('Image', 'Image'),
    ('ZIP', 'Compressed File'),
]

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    branch = models.CharField(max_length=30, choices=BRANCH_CHOICES)
    role = models.CharField(max_length=15, default='Student')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploadingdate = models.DateField(auto_now_add=True)
    branch = models.CharField(max_length=30, choices=BRANCH_CHOICES)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField(upload_to='notes/')
    filetype = models.CharField(max_length=30, choices=FILE_TYPE_CHOICES)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    downloads = models.IntegerField(default=0)  # Track download count

    def __str__(self):
        return f"{self.user.username} - {self.subject} ({self.status})"

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-uploadingdate']


class Contact(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    mobile = models.CharField(max_length=15)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    msgdate = models.DateField(auto_now_add=True)
    isread = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fullname} - {self.subject}"

    class Meta:
        verbose_name = 'Contact Query'
        verbose_name_plural = 'Contact Queries'
        ordering = ['-msgdate']