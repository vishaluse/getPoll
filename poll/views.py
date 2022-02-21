from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.shortcuts import redirect, render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse

from poll.models import Poll, Option, PollHistory
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages


class PollListView(ListView):
    model = Poll
    template_name = 'poll/main.html'


def singlePollDetail(request, pk):
    poll = Poll.objects.get(pk=pk)
    image = poll.get_image()
    visitor = False
    if request.user.is_authenticated: 
        try:
            poll_history = PollHistory.objects.get(user=request.user, poll=poll)
        except PollHistory.DoesNotExist:
            poll_history = PollHistory.objects.create(user=request.user, poll=poll)
    else :
        visitor = True
        poll_history = False
    
    context = {'poll': poll, 'image': image, 'poll_history': poll_history, 'visitor': visitor}
    return render(request, 'poll/poll_page.html', context)



def poll_data_view(request,pk):
    poll = Poll.objects.get(pk=pk)
    flag = False
    if request.user.is_authenticated: 
        try:
            poll_history = PollHistory.objects.get(user=request.user, poll=poll)
        except PollHistory.DoesNotExist:
            poll_history = PollHistory.objects.create(user=request.user, poll=poll)
        
        flag = poll_history.is_voted

    
    ans = []
    for i in poll.get_option():
        ans.append(i.text)
    
   
    context = {str(poll.question): ans}
    #after a minute pass the time as time--
    return JsonResponse({
        'data': context,
        'time': poll.time,
        'is_voted': flag
    })




def save_poll_data(request, pk):
    if request.user.is_authenticated and request.is_ajax():
        data = request.POST
        poll = Poll.objects.get(pk=pk)
       
        poll_history = PollHistory.objects.get(user=request.user, poll=poll)
       
        # create a poll_history only if it does not exit which will contain the current user and the poll he/she is voting for
        # and check if he/she has voted then don't let them vote again 
        # else let them vote

        if poll_history.is_voted == False:
            for i in poll.get_option():
                if i.text == data[poll.question]:
                    i.count += 1
                    i.save()
            for i in poll.get_image():
                if str(i.image) == str(data[poll.question]):
                    i.count += 1
                    i.save()
            poll_history.is_voted = True
            poll_history.save()
            messages.warning(request, 'You just voted')
            return JsonResponse({'data': 'your vot got saved, congrats' })
            
        else :
            return JsonResponse({'data': 'You have already voted'})
    else:
        return JsonResponse({'data': 'Sign up or login vro'})
        # i need the all the option here which is associated with this question and
        # then I'll do the count ++ manually of the selected option
    
        
    

def result_data(request,pk):
    #using pk we will get the the question then we will see their count;
    poll = Poll.objects.get(pk=pk)

    option = poll.get_option()

    total = 0
    for op in option:
        total += op.count

    image = poll.get_image()
       
    context = {'polls': poll, 
               'option': option, 
               'image': image, 
               'total': total}
    
    return render(request, 'poll/result.html', context)

def check_create_poll(request):
    if request.user.is_anonymous:
        messages.warning(request, 'You must log in to create polls.')
    return create_poll(request)


@login_required()
def create_poll(request):
    if request.method == "POST":
        question = request.POST.get('question')
        options  = request.POST.getlist('options')
        time = request.POST.get('timer')
        poll = Poll.objects.create(question=question, no_of_option=len(options), time=time, user=request.user)
        
        for option in options:
            Option.objects.create(text=option, poll=poll)

    return render(request, 'poll/create_poll.html')
    
def result_json(request, pk):
    poll = Poll.objects.get(pk=pk)
    option = poll.get_option()
    option_data = []
    for op in option:
        option_data.append({op.text: op.count})
    
    return JsonResponse(option_data, safe=False)


def profile_dashboard(request):
    context = {}
    return render(request, 'poll/profile_dashboard.html', context)

def profile_info(request):
    return render(request, 'account/profile_info.html');