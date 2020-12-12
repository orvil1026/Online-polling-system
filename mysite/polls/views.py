
from django.contrib.auth import login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import Quiz,Poll, Choice, Vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm,EnterQuizForm
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import JsonResponse
# Create your views here.

@login_required()
def quiz(request):
    quiz_exists=False
    all_quiz_id=Quiz.objects.all()

    if request.method=='POST':

        form=EnterQuizForm(request.POST)

        if form.is_valid():

            entered_quiz_id=form.cleaned_data['quiz_id']
            try:
                
                quiz_id=Quiz.objects.get(quiz_id__exact=entered_quiz_id)
                q_id=quiz_id.id
                all_polls=quiz_id.poll_set.all()
                messages.success(request,'WELCOME!',
                                extra_tags='alert alert-success alert-dismissible fade show')
                context={
                    'quiz_id':quiz_id,
                    'all_polls':all_polls,
                    'q_id':q_id
                    }
                quiz_exists=True     
                return HttpResponseRedirect(reverse('polls:list', args=(quiz_id,)))
            except ObjectDoesNotExist :
                messages.error(request,'Registration failed!',
                        extra_tags='alert alert-warning alert-dismissible fade show')
                return redirect('polls:quiz')

    else:
        form=EnterQuizForm()
    return render(request,'polls/quiz_id.html',{'form':form})

    

@login_required()
def polls_list(request,quiz_id):
    quiz=Quiz.objects.get(quiz_id__exact=quiz_id)
    all_polls=quiz.poll_set.all().order_by('id')
    
    request.session['quizId']=quiz_id

    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)


    paginator = Paginator(all_polls, 6)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
    }
    return render(request, 'polls/polls_list.html', context)

@login_required()
def poll_detail(request,poll_id):

    quiz_id=request.session['quizId']
    poll=get_object_or_404(Poll,id=poll_id)
    if not poll.active :
        return render(request,'polls/poll_result.html',{'poll':poll,'quiz_id':quiz_id})

   

    loop_count=poll.choice_set.count()
    context={
        'poll':poll,
        'loop_time':range(0,loop_count),
        'quiz_id':quiz_id
    }

    return render(request,'polls/poll_detail.html',context)

@login_required()
def poll_vote(request,poll_id):
    poll=get_object_or_404(Poll,pk=poll_id)
    choice_id=request.POST.get('choice')
    quiz_id=request.session['quizId']

    if not poll.user_can_vote(request.user):
        messages.error(
            request,"You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
        return render(request,"polls/poll_result.html",{'poll':poll,'quiz_id':quiz_id,'poll_id':poll_id})


    if choice_id:
        choice=Choice.objects.get(id=choice_id)
        vote=Vote(user=request.user,poll=poll,choice=choice)
        vote.save()
        print(vote)
        return render(request,"polls/poll_result.html",{'poll':poll,'quiz_id':quiz_id,'poll_id':poll_id})
    else:
        messages.error(
            request, "No choice selected", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:detail", poll_id)

    return render(request,"polls/poll_result.html",{'poll':poll,'quiz_id':quiz_id,'poll_id':poll_id})

    
@login_required()
def resultsData(request,poll_id):

    votedata=[]
    poll=get_object_or_404(Poll,pk=poll_id)
    votes=poll.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.get_vote_count})
    print(votedata)

    return JsonResponse(votedata,safe=False)


