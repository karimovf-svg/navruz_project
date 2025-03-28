from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def admin_panel(request):
    messages = ContactMessage.objects.all().order_by('-created_at')  # Eng yangi xabarlar birinchi chiqadi
    return render(request, 'admin_panel.html', {'messages': messages})

def staff_panel(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'admin_panel.html', {'messages': ContactMessage.objects.all()})
    else:
        form = ContactForm()  # GET so‘rovlar uchun formani yaratish

    return render(request, 'staff_panel.html', {'form': form})

def blog(request):
    return render(request, 'blog.html')

def blog_details(request):
    return render(request, 'blog-details.html')

def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin:
                    return redirect('admin_panel')
                elif user.is_staff:
                    return redirect('staff_panel')
            else:
                messages.error(request, "Telefon raqam yoki parol noto'g'ri")
        else:
            messages.error(request, "Forma noto'g'ri to'ldirilgan")
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def add_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Foydalanuvchi muvaffaqiyatli qo'shildi")
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreateForm()
    return render(request, 'add_user.html', {'form': form})


def contact_view(request):
    form = ContactForm()
    success_message = None

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )

            # Email jo‘natish
            send_mail(
                f"New Contact Form Submission: {contact.subject}",
                f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
                'your-email@example.com',
                ['admin@example.com'],
                fail_silently=False,
            )

            success_message = "Your message has been sent. Thank you!"
            return redirect('contact')  # Forma yuborilgandan keyin sahifani yangilaydi

    return render(request, 'staff_panel#contact.html', {'form': form, 'success_message': success_message})


@login_required
def messages_view(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'admin_panel.html', {'messages': messages})


@login_required
def client_message(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)
    replies = MessageReply.objects.filter(message=message).order_by('created_at')
    return render(request, 'client_massege.html', {
        'message': message,
        'replies': replies
    })


@login_required
def reply_message(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(ContactMessage, id=message_id)
        content = request.POST.get('reply_content')
        if content:
            MessageReply.objects.create(
                message=message,
                content=content,
                replied_by=request.user
            )
            message.replied = True
            message.save()

            # Email jo'natish
            send_mail(
                f"Javob: {message.subject}",
                f"Xabaringizga javob:\n\n{content}\n\nHurmat bilan,\n{request.user.name}",
                'your-email@example.com',
                [message.email],
                fail_silently=False,
            )

            messages.success(request, "Javob muvaffaqiyatli yuborildi va email jo'natildi")
        return redirect('client_massege', message_id=message.id)
    return redirect('messages')

