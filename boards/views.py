from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import Board, Topic, Post


# Create your views here.
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})


def new_topic(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first() # TODO: Need to get the currently logged in user

        topic = Topic.objects.create(subject=subject, board=board, starter=user)

        post = Post.objects.create(message=message, topic=topic, created_by=user)
        return redirect('board_topics', pk=board.pk) # TODO: Need to redirect to the created topic page

    return render(request, 'new_topic.html', {'board': board})
