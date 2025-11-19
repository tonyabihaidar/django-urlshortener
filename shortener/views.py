import re
from io import BytesIO

import qrcode
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET

from .forms import ShortURLForm
from .models import ShortURL


# ---------- Auth views ----------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('shortener:home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shortener:home')
    else:
        form = UserCreationForm()

    return render(request, 'shortener/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('shortener:home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shortener:home')
    else:
        form = AuthenticationForm(request)

    return render(request, 'shortener/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('shortener:login')


# ---------- Core app views ----------

@login_required
def home(request):
    """
    Show form to create a short URL (user must be logged in).
    """
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            short = form.save(user=request.user)
            return redirect('shortener:detail', slug=short.slug)
    else:
        form = ShortURLForm()

    return render(request, 'shortener/home.html', {
        'form': form,
    })


@login_required
def my_links(request):
    """
    List only the links created by the current user (private analytics).
    """
    links = ShortURL.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shortener/my_links.html', {
        'links': links,
    })


@login_required
def detail(request, slug):
    """
    Show details for ONE link belonging to the current user.
    """
    short = get_object_or_404(ShortURL, slug=slug, user=request.user)
    short_url = request.build_absolute_uri(
        reverse('shortener:redirect', args=[short.slug])
    )
    qr_url = reverse('shortener:qr', args=[short.slug])

    return render(request, 'shortener/detail.html', {
        'short': short,
        'short_url': short_url,
        'qr_url': qr_url,
    })


def redirect_view(request, slug):
    """
    Public: anyone can use the short link.
    """
    short = get_object_or_404(ShortURL, slug=slug)
    short.clicks += 1
    short.save(update_fields=['clicks'])
    return redirect(short.target_url)


def qr_code_view(request, slug):
    """
    Public: return PNG QR code for the short URL.
    """
    short = get_object_or_404(ShortURL, slug=slug)
    short_url = request.build_absolute_uri(
        reverse('shortener:redirect', args=[short.slug])
    )

    img = qrcode.make(short_url)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')


@require_GET
@login_required
def check_slug(request):
    """
    AJAX endpoint: check if a custom slug is valid & available.
    """
    slug = request.GET.get('slug', '').strip()
    valid = False
    available = False
    message = ''

    if not slug:
        message = 'Enter a custom code to check.'
    elif not re.match(r'^[a-zA-Z0-9_-]+$', slug):
        message = 'Only letters, numbers, hyphen, underscore allowed.'
    else:
        valid = True
        exists = ShortURL.objects.filter(slug=slug).exists()
        available = not exists
        message = 'Available!' if available else 'Already taken.'

    return JsonResponse({
        'valid': valid,
        'available': available,
        'message': message,
    })
