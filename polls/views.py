from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.http import HttpResponseRedirect

from .models import Question, Choice, Vote, User

def get_message(request):
    if request.session.get('user') is None:
            msg = "Hallo. Du bist nicht eingeloggt und daher nicht stimmberechtigt. Melde dich im ZaPF-Auth an, falls du abstimmen können möchtest."
    else:
        user, created = User.objects.get_or_create(user_name=request.session.get('user'))
        if user.voting_rights:
            msg = f"Hallo {request.session['user']['firstName']}, du bist stimmberechtigt."
        else:
            msg = f"Hallo {request.session['user']['firstName']}, du bist nicht stimmberechtigt, weil jemand deinen Account als nicht stimmberechtigt markiert hat."
    return msg

def results(request):
    if request.session.get('user') is not None:
        user, created = User.objects.get_or_create(user_name=request.session.get('user'))

    current_questions = [question for question in Question.objects.all() if question.active]
    questions = [question for question in Question.objects.all() if not question.active]
    if len(questions) < 1:
        questions = None
    else:
        questions = reversed(questions)
    context = {
        'message': get_message(request),
        'current_questions': current_questions,
        'questions': questions,
    }
    return render(request, 'polls/results.html', context)

def open_polls(request):
    if request.session.get('user') is not None:
        user, created = User.objects.get_or_create(user_name=request.session.get('user'))

    questions = [question for question in Question.objects.all() if question.active]
    context = {
        'message': get_message(request),
        'questions': questions,
    }
    return render(request, 'polls/open_polls.html', context)

def vote(request, question_id):
    if request.session.get('user') is not None:
        user, created = User.objects.get_or_create(user_name=request.session.get('user'))

    question = get_object_or_404(Question, pk=question_id)
    
    if not question.active:
        context = {
            'message': get_message(request),
            'question': question,
            'error_message': "Diese Abstimmung ist geschlossen.",
        }
        print(context)
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', context)

    if not user.voting_rights:
        context = {
            'message': get_message(request),
            'question': question,
            'error_message': "Du bist nicht stimmberechtigt.",
        }
        print(context)
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', context)
    
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'message': get_message(request),
            'question': question,
            'error_message': "You didn't select a valid choice.",
        }
        
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', context)
    else:
        votes = Vote.objects.filter(choice__question = question, user = user)
        if len(votes) > 1:
            raise Exception("Multiple Votes detected")
        elif len(votes) == 1:
            new_vote = votes[0]
            new_vote.choice = selected_choice
        else:
            new_vote, created = votes.get_or_create(user=user, defaults={'choice': selected_choice})   
        new_vote.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results'))
