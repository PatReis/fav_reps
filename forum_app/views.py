from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Message
from .forms import RoomForm
from recipes_app.models import Topic
from .pagination import Pagination


def rooms(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    pgNr = int(request.GET.get('pgNr')) if request.GET.get('pgNr') is not None else 0

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    room_count = rooms.count()
    # room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]

    pgShow = 25
    page_size = max(min(int(pgShow), 10), 200)
    page_choices = 10
    browser = Pagination(room_count, page_size, number_page_choices=page_choices)
    pgNr = browser.valid_page(pgNr)
    num_pages = browser.number_of_pages
    rooms_page = browser.get_items_for_page(rooms, pgNr)
    browser_context = browser.make_page_browser(pgNr)

    context = {'rooms': rooms_page,
               'room_count': room_count,
               #'room_messages': room_messages
               }
    context.update(browser_context)
    return render(request, 'forum_app/rooms.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    pgNr = int(request.GET.get('pgNr')) if request.GET.get('pgNr') is not None else 0

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    pgShow = 100
    page_size = max(min(int(pgShow), 10), 200)
    page_choices = 10
    browser = Pagination(room_messages.count(), page_size, number_page_choices=page_choices)
    pgNr = browser.valid_page(pgNr)
    num_pages = browser.number_of_pages
    room_messages_page = browser.get_items_for_page(room_messages, pgNr)
    browser_context = browser.make_page_browser(pgNr)

    context = {'room': room, 'room_messages': room_messages_page,
               'participants': participants}
    context.update(browser_context)
    return render(request, 'forum_app/room.html', context)

@login_required(login_url='user-login-required')
def createRoom(request):

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            recipe_saved = form.save()

            recipe_saved.owner = request.user
            recipe_saved.save()
            return redirect('rooms')
    else:
        form = RoomForm()

    context = {'form': form}
    return render(request, 'forum_app/room_form.html', context)


@login_required(login_url='user-login-required')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()

        return redirect('rooms')

    context = {'form': form, 'room': room}
    return render(request, 'forum_app/room_form.html', context)


@login_required(login_url='user-login-required')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Fehlende Berechtigung! Bitte wenden Sie sich and den Administrator.')

    if request.method == 'POST':
        room.delete()
        return redirect('rooms')
    return render(request, 'forum_app/delete.html', {'obj': room})


@login_required(login_url='user-login-required')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Fehlende Berechtigung! Bitte wenden Sie sich and den Administrator.')

    if request.method == 'POST':
        message.delete()
        return redirect('rooms')
    return render(request, 'forum_app/delete.html', {'obj': message})
