from django import forms
from .models import ShortURL


class ShortURLForm(forms.ModelForm):
    custom_slug = forms.SlugField(
        max_length=10,
        required=False,
        label="Custom short code (optional)"
    )

    class Meta:
        model = ShortURL
        fields = ['target_url', 'custom_slug']
        labels = {
            'target_url': 'Long URL',
        }

    def clean_custom_slug(self):
        slug = self.cleaned_data.get('custom_slug')
        if slug and ShortURL.objects.filter(slug=slug).exists():
            raise forms.ValidationError("This slug is already taken.")
        return slug

    def save(self, user=None, commit=True):
        """
        Attach the link to the given user (if provided).
        """
        instance = super().save(commit=False)
        slug = self.cleaned_data.get('custom_slug')
        if slug:
            instance.slug = slug
        if user is not None and instance.user_id is None:
            instance.user = user
        if commit:
            instance.save()
        return instance
