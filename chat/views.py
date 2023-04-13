from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Room
from .random_string import generate_random_string

@login_required
def room(request, room_name):
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        raise Http404("Room does not exist")
    if request.user not in [room.requester, room.responder]:
        raise Http404("You are not allowed to view this room")
    return render(request, "room.html", {"room": room }) 


@login_required
def requester(request):
    if request.method == 'POST':
        room_name = generate_random_string()
        try:
            room = Room.objects.get(requester=request.user)
        except Room.DoesNotExist:
            room = Room(name=room_name, requester=request.user)
            room.save()
        return redirect(reverse('room', kwargs={'room_name': room.name}))


@login_required
def responder(request):
    if request.method == 'POST':
        room = None
        rooms = Room.objects.all()
        for r in rooms:
            requester_age = r.requester.age
            requester_gender = r.requester.gender
            requester_age_pref = r.requester.age_pref
            requester_gender_pref = r.requester.gender_pref
            responder_age = request.user.age
            responder_gender = request.user.gender
            responder_age_pref = request.user.age_pref
            responder_gender_pref = request.user.gender_pref
            if responder_gender_pref:
                if requester_gender != responder_gender_pref:
                    continue
            if requester_gender_pref:
                if responder_gender != requester_gender_pref:
                    continue
            if responder_age_pref:
                if responder_age_pref == 0:
                    if requester_age != responder_age:
                        continue
                elif responder_age_pref == 1:
                    if requester_age >= responder_age:
                        continue
                elif responder_age_pref == 2:
                    if requester_age <= responder_age:
                        continue
                elif responder_age_pref == 3:
                    if requester_age > responder_age:
                        continue
                elif responder_age_pref == 4:
                    if requester_age < responder_age:
                        continue
                elif responder_age_pref == 5:
                    if requester_age == responder_age:
                        continue
            if requester_age_pref:
                if requester_age_pref == 0:
                    if responder_age != requester_age:
                        continue
                elif requester_age_pref == 1:
                    if responder_age >= requester_age:
                        continue
                elif requester_age_pref == 2:
                    if responder_age <= requester_age:
                        continue
                elif requester_age_pref == 3:
                    if responder_age > requester_age:
                        continue
                elif requester_age_pref == 4:
                    if responder_age < requester_age:
                        continue
                elif requester_age_pref == 5:
                    if responder_age == requester_age:
                        continue
            room = r
            break
        if room:
            room.responder = request.user
            room.save()
            return redirect(reverse('room', kwargs={'room_name': room.name}))
        else:
            return redirect('index')
            

