from django import forms
from django.contrib.auth.models import User
from .models import Signup, Notes, Contact, BRANCH_CHOICES, CATEGORY_CHOICES, FILE_TYPE_CHOICES


class SignupForm(forms.ModelForm):
    """Form for user registration"""
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        min_length=8
    )
    contact = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'})
    )
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Signup
        fields = ['contact', 'branch']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact


class NotesUploadForm(forms.ModelForm):
    """Form for uploading documents"""
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'})
    )
    filetype = forms.ChoiceField(
        choices=FILE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notesfile = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief description of the document'})
    )

    class Meta:
        model = Notes
        fields = ['branch', 'category', 'subject', 'filetype', 'notesfile', 'description']

    def clean_notesfile(self):
        file = self.cleaned_data.get('notesfile')
        if file:
            # Check file size (50 MB max)
            max_size = 50 * 1024 * 1024
            if file.size > max_size:
                raise forms.ValidationError("File size must not exceed 50 MB.")

            # Check file extension
            allowed_extensions = ['.pdf', '.ppt', '.pptx', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png', '.zip', '.rar']
            file_name = file.name.lower()
            if not any(file_name.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError("Invalid file type. Allowed: PDF, PPT, DOC, TXT, Images, ZIP/RAR")
        return file


class ContactForm(forms.ModelForm):
    """Form for contact/query submission"""
    fullname = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'})
    )
    subject = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'})
    )

    class Meta:
        model = Contact
        fields = ['fullname', 'email', 'mobile', 'subject', 'message']


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile"""
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch = forms.ChoiceField(
        choices=BRANCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Signup
        fields = ['contact', 'branch']

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")
        if len(contact) != 10:
            raise forms.ValidationError("Contact number must be exactly 10 digits.")
        return contact


class PasswordChangeForm(forms.Form):
    """Form for changing password"""
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'})
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        min_length=8
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError("New passwords don't match!")

        return cleaned_data


class SearchFilterForm(forms.Form):
    """Form for searching and filtering documents"""
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by subject or description'})
    )
    branch = forms.ChoiceField(
        choices=[('', 'All Branches')] + BRANCH_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    filetype = forms.ChoiceField(
        choices=[('', 'All File Types')] + FILE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
