from io import BytesIO

import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse

from .forms import ShortURLForm
from .models import ShortURL


def home(request):
    """
    Show form to create a short URL and list latest ones.
    """
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            short = form.save()
            return redirect('shortener:detail', slug=short.slug)
    else:
        form = ShortURLForm()

    latest_links = ShortURL.objects.order_by('-created_at')[:10]
    # Base URL like "http://127.0.0.1:8000"
    base_url = request.build_absolute_uri('/').rstrip('/')

    return render(request, 'shortener/home.html', {
        'form': form,
        'latest_links': latest_links,
        'base_url': base_url,
    })


def detail(request, slug):
    """
    Show details for one shortened URL (including QR).
    """
    short = get_object_or_404(ShortURL, slug=slug)
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
    Redirect /<slug>/ to the target URL and increment click counter.
    """
    short = get_object_or_404(ShortURL, slug=slug)
    short.clicks += 1
    short.save(update_fields=['clicks'])
    return redirect(short.target_url)


def qr_code_view(request, slug):
    """
    Return a PNG QR code for the short URL.
    """
    short = get_object_or_404(ShortURL, slug=slug)
    short_url = request.build_absolute_uri(
        reverse('shortener:redirect', args=[short.slug])
    )

    # Generate QR code
    img = qrcode.make(short_url)
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')
