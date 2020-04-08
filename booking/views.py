from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import SignUpForm
from datetime import datetime
from booking.models import slots
from django.db import transaction
from django.contrib.auth.models import User


class SlotBooking(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def save_slots_for_user(self, user, slotsIP, dateIP):
        user1 = User.objects.get(id = user.id)
        datetime_str = dateIP + " " + slotsIP
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
        s = slots.objects.get(user = user1, dateFromSlot = datetime_object)
        if s.booked == True:
            raise Exception('slot already booked or not existing')
            return
        s.booked = True
        s.save()

    # TODO - slots can be inbetween slots, logic to be written to handle that
    def post(self, request):
        user = request.user
        slotsIP = request.data['slot']
        dateIP = request.data['date']
        status = False
        try:
            self.save_slots_for_user(user, slotsIP, dateIP)
            status = True
        except Exception as e:
            print(str(e))
            print(slots.objects.filter(user = user))
        return Response(data={"status": status})


class ListSlot(APIView):
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def save_slots_for_user(self, user, slotsIP, dateIP):
        user1 = User.objects.get(id = user.id)
        for slot in slotsIP:
            datetime_str = dateIP + " " + slot
            datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')
            s = slots(user = user1, dateFromSlot = datetime_object, booked = False)
            s.save()


    # TODO - slots can be inbetween slots, logic to be written to handle that
    def post(self, request):
        user = request.user
        slotsIP = request.data['slots']
        dateIP = request.data['date']
        status = False
        try:
            self.save_slots_for_user(user, slotsIP, dateIP)
            status = True
        except Exception as e:
            print(str(e))
            print(slots.objects.filter(user = user))
        return Response(data={"status": status})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/admin/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})