"""
Email utility functions for sending notifications
"""
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)


def send_document_status_email(note, status):
    """
    Send email notification when document status changes

    Args:
        note: Notes model instance
        status: New status (Accept/Reject)
    """
    try:
        subject = f"Document Status Update - {note.subject}"

        if status == 'Accept':
            message = f"""
Hello {note.user.first_name},

Good news! Your document has been approved.

Document Details:
- Subject: {note.subject}
- Branch: {note.branch}
- Category: {note.category}
- Uploaded on: {note.uploadingdate}

Your document is now visible to all students and available for download.

Thank you for contributing to the academic resource portal!

Best regards,
SemStar Team
            """
        else:  # Reject
            message = f"""
Hello {note.user.first_name},

We regret to inform you that your document has been rejected.

Document Details:
- Subject: {note.subject}
- Branch: {note.branch}
- Category: {note.category}
- Uploaded on: {note.uploadingdate}

Please ensure your document meets quality standards and try uploading again.

Best regards,
SemStar Team
            """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[note.user.email],
            fail_silently=False,
        )

        logger.info(f"Status email sent to {note.user.email} for document {note.id}")
        return True

    except Exception as e:
        logger.error(f"Failed to send status email: {e}")
        return False


def send_welcome_email(user):
    """
    Send welcome email to new users

    Args:
        user: User model instance
    """
    try:
        subject = "Welcome to SemStar - Academic Resource Portal"
        message = f"""
Hello {user.first_name},

Welcome to SemStar! Your account has been successfully created.

You can now:
- Upload educational documents (notes, model papers, guidance materials)
- Access approved documents from other students
- Organize resources by branch and category

Please note that all uploaded documents go through an admin approval process before becoming visible to other students.

Get started by logging in at: [Your Portal URL]

Best regards,
SemStar Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Welcome email sent to {user.email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send welcome email: {e}")
        return False


def send_contact_confirmation_email(contact):
    """
    Send confirmation email when contact form is submitted

    Args:
        contact: Contact model instance
    """
    try:
        subject = "Thank you for contacting SemStar"
        message = f"""
Hello {contact.fullname},

Thank you for reaching out to us!

We have received your message regarding: {contact.subject}

Our team will review your query and get back to you soon at {contact.email}.

Best regards,
SemStar Team
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[contact.email],
            fail_silently=False,
        )

        logger.info(f"Contact confirmation email sent to {contact.email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send contact confirmation email: {e}")
        return False


def send_new_document_notification_to_admin():
    """
    Send email to admins when new document is uploaded
    (Optional - can be implemented if needed)
    """
    pass
