from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category, Tag


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class PostForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        label='Tags',
        help_text='Comma-separated tags (e.g. django, python, web)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'django, python, web'})
    )

    class Meta:
        model = Post
        fields = ['title', 'category', 'excerpt', 'content', 'cover_image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short description (optional)'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 15, 'placeholder': 'Write your post content here...'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = '— No category —'
        if self.instance.pk:
            existing_tags = ', '.join(tag.name for tag in self.instance.tags.all())
            self.fields['tags_input'].initial = existing_tags

    def save(self, commit=True):
        post = super().save(commit=commit)
        if commit:
            tags_input = self.cleaned_data.get('tags_input', '')
            post.tags.clear()
            if tags_input:
                for tag_name in [t.strip() for t in tags_input.split(',') if t.strip()]:
                    from django.utils.text import slugify
                    tag, _ = Tag.objects.get_or_create(
                        slug=slugify(tag_name),
                        defaults={'name': tag_name}
                    )
                    post.tags.add(tag)
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts…', 'style': 'resize:vertical;'}),
        }

class GuestCommentForm(forms.ModelForm):
    """Full form for unauthenticated users — requires name, email, body."""
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com', 'required': True}),
            'body':  forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts…', 'style': 'resize:vertical;'}),
        }

class UserCommentForm(forms.ModelForm):
    """Simplified form for logged-in users — only needs the message body."""
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your thoughts on this post…', 'style': 'resize:vertical;'}),
        }
