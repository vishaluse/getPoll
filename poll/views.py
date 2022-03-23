from glob import glob
from re import template
from django.contrib.auth.forms import UserCreationForm
from django.http.response import HttpResponse
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, render
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
# from matplotlib import image

from poll.models import ImageOption, Poll, Option, PollHistory
from django.contrib.auth.decorators import login_required
from django.contrib import messages #import messages
import itertools 
import datetime



# it will pass all the poll object in the model , cause its a listView
class PollListView(ListView):
    model = Poll
    template_name = 'poll/main.html'
    ordering = ['-created']


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
    if request.user.is_authenticated and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = request.POST
        # print(data)
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
            return JsonResponse({'data': 'your vote got saved, congrats' })
            
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
    image = poll.get_image()

    total = 0
    for op in option:
        total += op.count
    for op in image:
        total += op.count

    
       
    context = {'polls': poll, 
               'option': option, 
               'image': image, 
               'total': total}
    
    return render(request, 'poll/result.html', context)


    
def result_json(request, pk):
    poll = Poll.objects.get(pk=pk)
    option = poll.get_option()
    image  = poll.get_image()
    option_data = []
    for op in option:
        option_data.append({op.text: op.count})
    for op in image:
        option_data.append({str(op.image): op.count})
    
    return JsonResponse(option_data, safe=False)


def profile_dashboard(request):
    context = {}
    return render(request, 'poll/profile_dashboard.html', context)

def profile_info(request):
    return render(request, 'account/profile_info.html');


# CRUD operations for polls


def check_create_poll(request):
    if request.user.is_anonymous:
        messages.info(request, 'You must log in to create polls.')
    return create_poll(request)


@login_required()
def create_poll(request):
    if request.method == "POST":
        question = request.POST.get('question')
        options  = request.POST.getlist('options')
        images  = request.FILES.getlist('images')
        time = request.POST.get('timer')

        print(images)
        # return redirect('/')
        poll = Poll.objects.create(question=question, no_of_option=len(options), time=time, user=request.user)
        
        for option in options:
            Option.objects.create(text=option, poll=poll)
        
        for image in images: 
            ImageOption.objects.create(image=image, poll=poll)

        messages.success(request, 'Your poll is created !')
        return redirect('/')

    return render(request, 'poll/create_poll.html')


# dashboard for current user to manipulates his/her created polls
@login_required
def userPoll(request):
    polls = Poll.objects.filter(user=request.user).order_by('-created')
    # userPolls = []
    # for poll in polls:
    #     if poll.user == request.user:
    #         userPolls.append(poll.order)

    context = {'polls' :polls}
    return render(request, 'poll/poll_dashboard.html', context)

# class PollDetailView(DetailView):
#     model = Poll
#     template_name = 'poll/poll_update.html'

def updateOption(option_list, option_given_list, poll, givenModel) :
    for (a, b) in itertools.zip_longest(option_list, option_given_list):
            if a != None and b != None :
                if givenModel == ImageOption:
                    a.image = b
                else:
                    a.text = b
                a.save()
            elif a != None:
                a.delete()
            elif b != None:
                if givenModel == ImageOption:
                    ImageOption.objects.create(image=b, poll=poll)
                else:
                    Option.objects.create(text=b, poll=poll)



def userPollDetail(request, pk):
    poll = Poll.objects.get(pk=pk)
    option_list = poll.get_option()
    image_list = poll.get_image()
    
    # if user has submitted the form then this will get called
    if request.method == "POST":
        # it will check if the fields are changed, if they are, it will update the current poll
        question = request.POST.get('question')
        time = request.POST.get('timer')

        poll.question = question
        poll.time = time

        poll.created = datetime.datetime.now()
        poll.save()

        image_img_list  = request.FILES.getlist('images')
        option_text_list  = request.POST.getlist('options')

        # it is performing how many option user has gave to the form so it will make those option connect with the poll either its a text or image
        if option_list :
            updateOption(option_list, option_text_list, poll, Option)
        
        if image_list :
            updateOption(image_list, image_img_list, poll, ImageOption)
        
        messages.warning(request, "your poll is updated")

  
    current_option_list = poll.get_option()
    if option_list:
        current_option_list = poll.get_option()
    elif image_list:
        current_option_list = poll.get_image()



    options = []
    cnt = 0
    global first
    first = poll.get_option()
    global second
    second = poll.get_option()


    for option in current_option_list:
        if cnt == 0: 
            first = option
            cnt += 1
        elif cnt == 1:
            second = option
            cnt += 1
        else:
            options.append(option)  
        
    
    context = {'poll': poll,
               'options': options,
               'first': first,
               'second': second,   
               'optionList': option_list,
               
    }

    return render(request, 'poll/poll_update.html', context)


@login_required
def deletePoll(request, pk):
    try:
        poll = Poll.objects.get(pk=pk)
        poll.delete()
        messages.info(request, "Poll is deleted successfully !")
    except Poll.DoesNotExist:
        pass
    return redirect('user-poll')





