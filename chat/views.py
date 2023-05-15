from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import Room
from .random_string import generate_random_string
from django.views import View
from django.db.models import Q

class RoomView(View):
    def get(self, request, room_name):
        try:
            room = Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            raise Http404("Room does not exist")
        if request.user not in [room.requester, room.responder]:
            raise Http404("You are not allowed to view this room")
        return render(request, "chat/room.html", {"room": room })
    

class GetRoom(View):
    def get(self, request):
        try:
            room = Room.objects.filter(Q(requester=request.user) | Q(responder=request.user)).first()
        except Room.DoesNotExist:
            room = None
        if room:
            return JsonResponse({'room_name': room.name})
        else:
            return JsonResponse({'room_name': None})
        

class CreateRoom(View):
    def post(self, request):
        room_name = generate_random_string()
        room = Room(name=room_name, requester=request.user)
        room.save()
        return JsonResponse({'room_name': room.name})
    

class RespondRoom(View):
    def post(self, request):
        room = None
        rooms = Room.objects.all()
        for r in rooms:
            requester_dob = r.requester.dob
            requester_gender = r.requester.gender
            requester_age_pref = r.requester.age_pref
            requester_gender_pref = r.requester.gender_pref
            responder_dob = request.user.dob
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
                date_diff = requester_dob - responder_dob
                days_diff = date_diff.days
                if responder_age_pref == 0:
                    if abs((requester_dob - responder_dob).days) > 365:
                        continue
                elif responder_age_pref == 1:
                    if days_diff >= -365:
                        continue
                elif responder_age_pref == 2:
                    if days_diff <= 365:
                        continue
                elif responder_age_pref == 3:
                    if days_diff > 365:
                        continue
                elif responder_age_pref == 4:
                    if days_diff < -365:
                        continue
                elif responder_age_pref == 5:
                    if abs((requester_dob - responder_dob).days) < 365:
                        continue
            if requester_age_pref:
                if requester_age_pref == 0:
                    if abs((responder_dob - requester_dob).days) > 365:
                        continue
                elif requester_age_pref == 1:
                    if responder_dob - requester_dob >= -365:
                        continue
                elif requester_age_pref == 2:
                    if responder_dob - requester_dob <= 365:
                        continue
                elif requester_age_pref == 3:
                    if responder_dob - requester_dob > 365:
                        continue
                elif requester_age_pref == 4:
                    if responder_dob - requester_dob < -365:
                        continue
                elif requester_age_pref == 5:
                    if abs((responder_dob - requester_dob).days) < 365:
                        continue
            room = r
            break
        if room:
            room.responder = request.user
            room.save()
            return JsonResponse({'room_name': room.name})
        else:
            return JsonResponse({'room_name': None})


class CloseRoom(View):
    def get(self, request):
        try:
            room = Room.objects.get(Q(requester=request.user) | Q(responder=request.user))
        except Room.DoesNotExist:
            room = None
        if room:
            room.delete()
            return JsonResponse({'room_name': room.name})
        else:
            return JsonResponse({'room_name': None})
