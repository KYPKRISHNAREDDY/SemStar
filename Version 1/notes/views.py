from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Signup, Notes, Contact
from .forms import SignupForm, NotesUploadForm, ContactForm, ProfileEditForm, PasswordChangeForm, SearchFilterForm
from .email_utils import send_document_status_email, send_welcome_email, send_contact_confirmation_email
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import date
import logging

# Configure logging
logger = logging.getLogger(__name__)


def about(request):
    """Display about page"""
    return render(request, 'about.html')


def index(request):
    """Display home page"""
    return render(request, 'index.html')


def contact(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                contact_obj = form.save()
                # Send confirmation email
                send_contact_confirmation_email(contact_obj)
                messages.success(request, 'Your message has been sent successfully!')
                return redirect('contact')
            except Exception as e:
                logger.error(f"Contact form error: {e}")
                messages.error(request, 'An error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def userlogin(request):
    """Handle user login"""
    error = ""
    if request.method == 'POST':
        username = request.POST.get('emailid', '').strip()
        password = request.POST.get('pwd', '')

        if not username or not password:
            error = "yes"
            messages.error(request, 'Please enter both email and password.')
        else:
            user = authenticate(username=username, password=password)
            if user and not user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('profile')
            else:
                error = "yes"
                messages.error(request, 'Invalid credentials or not a student account.')

    return render(request, 'login.html', {'error': error})


def login_admin(request):
    """Handle admin login"""
    error = ""
    if request.method == 'POST':
        username = request.POST.get('uname', '').strip()
        password = request.POST.get('pwd', '')

        if not username or not password:
            error = "yes"
            messages.error(request, 'Please enter both username and password.')
        else:
            user = authenticate(username=username, password=password)
            if user and user.is_staff:
                login(request, user)
                messages.success(request, f'Welcome, Admin {user.first_name}!')
                return redirect('admin_home')
            else:
                error = "yes"
                messages.error(request, 'Invalid credentials or not an admin account.')

    return render(request, 'login_admin.html', {'error': error})


def signup1(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                # Create user
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email']
                )

                # Create profile
                Signup.objects.create(
                    user=user,
                    contact=form.cleaned_data['contact'],
                    branch=form.cleaned_data['branch'],
                    role='Student'
                )

                # Send welcome email
                send_welcome_email(user)

                messages.success(request, 'Registration successful! Please check your email and login.')
                return redirect('login')
            except Exception as e:
                logger.error(f"Signup error: {e}")
                messages.error(request, 'An error occurred during registration.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def admin_home(request):
    """Admin dashboard with statistics"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    pn = Notes.objects.filter(status="pending").count()
    an = Notes.objects.filter(status="Accept").count()
    rn = Notes.objects.filter(status="Reject").count()
    alln = Notes.objects.all().count()
    total_users = Signup.objects.all().count()

    context = {
        'pn': pn,
        'an': an,
        'rn': rn,
        'alln': alln,
        'total_users': total_users
    }
    return render(request, 'admin_home.html', context)


def Logout(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')


def profile(request):
    """Display user profile"""
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    data = get_object_or_404(Signup, user=user)

    context = {'data': data, 'user': user}
    return render(request, 'profile.html', context)


def edit_profile(request):
    """Handle profile editing"""
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    signup_data = get_object_or_404(Signup, user=user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=signup_data)
        if form.is_valid():
            try:
                # Update user model
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.save()

                # Update signup model
                form.save()

                messages.success(request, 'Profile updated successfully!')
                return redirect('profile')
            except Exception as e:
                logger.error(f"Profile update error: {e}")
                messages.error(request, 'Error updating profile.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'contact': signup_data.contact,
            'branch': signup_data.branch
        }
        form = ProfileEditForm(instance=signup_data, initial=initial_data)

    context = {'form': form, 'data': signup_data, 'user': user}
    return render(request, 'edit_profile.html', context)


def changepassword(request):
    """Handle password change for users"""
    if not request.user.is_authenticated:
        return redirect('login')

    error = ""
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            if not request.user.check_password(old_password):
                error = "wrong"
                messages.error(request, 'Old password is incorrect.')
            else:
                request.user.set_password(new_password)
                request.user.save()
                error = "no"
                messages.success(request, 'Password changed successfully! Please login again.')
                return redirect('login')
        else:
            error = "yes"
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm()

    return render(request, 'changepassword.html', {'form': form, 'error': error})


def upload_notes(request):
    """Handle document upload"""
    if not request.user.is_authenticated:
        return redirect('login')

    error = ""
    if request.method == 'POST':
        form = NotesUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                note = form.save(commit=False)
                note.user = request.user
                note.status = 'pending'
                note.save()

                error = "no"
                messages.success(request, 'Document uploaded successfully! Awaiting admin approval.')
                return redirect('view_mynotes')
            except Exception as e:
                logger.error(f"Upload error: {e}")
                error = "yes"
                messages.error(request, 'Error uploading document.')
        else:
            error = "yes"
            messages.error(request, 'Please correct the errors below.')
    else:
        form = NotesUploadForm()

    return render(request, 'upload_notes.html', {'form': form, 'error': error})


def view_mynotes(request):
    """Display user's uploaded documents with pagination"""
    if not request.user.is_authenticated:
        return redirect('login')

    notes_list = Notes.objects.filter(user=request.user).order_by('-uploadingdate')

    # Pagination
    paginator = Paginator(notes_list, 10)  # Show 10 notes per page
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'view_mynotes.html', {'notes': notes})


def view_allnotes(request):
    """Display all notes (currently unused template - redirecting to viewallnotes)"""
    return redirect('viewallnotes')


def delete_mynotes(request, pid):
    """Delete user's own document"""
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        note = get_object_or_404(Notes, id=pid, user=request.user)
        note.delete()
        messages.success(request, 'Document deleted successfully!')
    except Exception as e:
        logger.error(f"Delete error: {e}")
        messages.error(request, 'Error deleting document.')

    return redirect('view_mynotes')


def view_users(request):
    """Admin view: Display all users with pagination"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    users_list = Signup.objects.all().select_related('user').order_by('-id')

    # Pagination
    paginator = Paginator(users_list, 15)  # Show 15 users per page
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'view_users.html', {'users': users})


def delete_users(request, pid):
    """Admin: Delete user account"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    try:
        user = get_object_or_404(User, id=pid)
        if user.is_staff:
            messages.error(request, 'Cannot delete admin users!')
        else:
            user.delete()
            messages.success(request, 'User deleted successfully!')
    except Exception as e:
        logger.error(f"User deletion error: {e}")
        messages.error(request, 'Error deleting user.')

    return redirect('view_users')


def pending_notes(request):
    """Admin view: Display pending documents with pagination"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    notes_list = Notes.objects.filter(status="pending").order_by('-uploadingdate')

    paginator = Paginator(notes_list, 10)
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'pending_notes.html', {'notes': notes})


def accepted_notes(request):
    """Admin view: Display accepted documents with pagination"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    notes_list = Notes.objects.filter(status="Accept").order_by('-uploadingdate')

    paginator = Paginator(notes_list, 10)
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'accepted_notes.html', {'notes': notes})


def rejected_notes(request):
    """Admin view: Display rejected documents with pagination"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    notes_list = Notes.objects.filter(status="Reject").order_by('-uploadingdate')

    paginator = Paginator(notes_list, 10)
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'rejected_notes.html', {'notes': notes})


def all_notes(request):
    """Admin view: Display all documents with pagination"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    notes_list = Notes.objects.all().order_by('-uploadingdate')

    paginator = Paginator(notes_list, 10)
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    return render(request, 'all_notes.html', {'notes': notes})


def assign_status(request, pid):
    """Admin: Assign approval status to documents"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    note = get_object_or_404(Notes, id=pid)
    error = ""

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['pending', 'Accept', 'Reject']:
            try:
                old_status = note.status
                note.status = status
                note.save()

                # Send email notification if status changed to Accept or Reject
                if status in ['Accept', 'Reject'] and old_status != status:
                    send_document_status_email(note, status)

                error = "no"
                messages.success(request, f'Document status changed to {status}! Email notification sent to user.')
                return redirect('pending_notes')
            except Exception as e:
                logger.error(f"Status assignment error: {e}")
                error = "yes"
                messages.error(request, 'Error updating status.')
        else:
            error = "yes"
            messages.error(request, 'Invalid status value.')

    return render(request, 'assign_status.html', {'notes': note, 'error': error})


def delete_notes(request, pid):
    """Admin: Delete any document"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    try:
        note = get_object_or_404(Notes, id=pid)
        note.delete()
        messages.success(request, 'Document deleted successfully!')
    except Exception as e:
        logger.error(f"Note deletion error: {e}")
        messages.error(request, 'Error deleting document.')

    return redirect('all_notes')


def viewallnotes(request):
    """Display all accepted documents with search and filtering"""
    if not request.user.is_authenticated:
        return redirect('login')

    # Get all accepted notes
    notes_list = Notes.objects.filter(status='Accept').order_by('-uploadingdate')

    # Search and filtering
    search_query = request.GET.get('search', '')
    branch_filter = request.GET.get('branch', '')
    category_filter = request.GET.get('category', '')
    filetype_filter = request.GET.get('filetype', '')

    if search_query:
        notes_list = notes_list.filter(
            Q(subject__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    if branch_filter:
        notes_list = notes_list.filter(branch=branch_filter)

    if category_filter:
        notes_list = notes_list.filter(category=category_filter)

    if filetype_filter:
        notes_list = notes_list.filter(filetype=filetype_filter)

    # Pagination
    paginator = Paginator(notes_list, 12)  # Show 12 notes per page
    page = request.GET.get('page')

    try:
        notes = paginator.page(page)
    except PageNotAnInteger:
        notes = paginator.page(1)
    except EmptyPage:
        notes = paginator.page(paginator.num_pages)

    # Create filter form
    form = SearchFilterForm(initial={
        'search_query': search_query,
        'branch': branch_filter,
        'category': category_filter,
        'filetype': filetype_filter
    })

    context = {
        'notes': notes,
        'form': form,
        'search_query': search_query,
        'branch_filter': branch_filter,
        'category_filter': category_filter,
        'filetype_filter': filetype_filter
    }
    return render(request, 'viewallnotes.html', context)


def change_passwordadmin(request):
    """Handle password change for admin"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    error = ""
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword', '')
        new_password = request.POST.get('newpassword', '')
        confirm_password = request.POST.get('confirmpassword', '')

        if not request.user.check_password(old_password):
            error = 'not'
            messages.error(request, 'Old password is incorrect.')
        elif new_password != confirm_password:
            error = 'yes'
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            error = 'yes'
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            try:
                request.user.set_password(new_password)
                request.user.save()
                error = "no"
                messages.success(request, 'Password changed successfully! Please login again.')
                return redirect('login_admin')
            except Exception as e:
                logger.error(f"Admin password change error: {e}")
                error = "yes"
                messages.error(request, 'Error changing password.')

    return render(request, 'change_passwordadmin.html', {'error': error})


def unread_queries(request):
    """Admin view: Display unread contact queries"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    contact = Contact.objects.filter(isread=False).order_by('-msgdate')
    return render(request, 'unread_queries.html', {'contact': contact})


def read_queries(request):
    """Admin view: Display read contact queries"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    contact = Contact.objects.filter(isread=True).order_by('-msgdate')
    return render(request, 'read_queries.html', {'contact': contact})


def view_queries(request, pid):
    """Admin view: View specific query and mark as read"""
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login_admin')

    contact = get_object_or_404(Contact, id=pid)
    contact.isread = True
    contact.save()

    return render(request, 'view_queries.html', {'contact': contact})
