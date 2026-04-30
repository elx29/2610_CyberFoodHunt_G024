# Create your views here.
from django.shortcuts import render, redirect
from .forms import PostForm
from .models import User

def review(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_id = User.objects.get(user_id=1)
            post.save()
            message = 'Post submitted successfully!'      # ← show message instead
            return render(request, 'review.html', {'form': PostForm(), 'message': message})
    else:
        form = PostForm()

    return render(request, 'review.html', {'form': form})