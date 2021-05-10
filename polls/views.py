from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from .models import Question, Choice, Vote, Uni

def get_message(request):
    if request.session.get('uni') is None:
        if request.session.get('user') is None:
            msg = f"Hallo, du bist nicht eingeloggt und daher nicht stimmberechtigt. Melde dich im ZaPF-Auth an, falls du abstimmen können möchtest."
        else:
            msg = f"Hallo {request.session['user']['full_name']}, du bist nicht für die ZaPF angemeldet und daher nicht stimmberechtigt."
    elif not request.session['confirmed']:
        msg = f"Hallo {request.session['user']['full_name']}, deine Fachschaft hat dich nicht bestätigt und du bist daher nicht stimmberechtigt."
    elif request.session['uni'] == 88:
        msg = f"Hallo {request.session['user']['full_name']}, du bist als alter Sack angemeldet und daher nicht stimmberechtigt."
    else:
        msg = f"Hallo {request.session['user']['full_name']}, du bist für {request.session['unis'][str(request.session['uni'])]} wahlberechtigt."
    return msg

def results(request):
    if request.session.get('uni') is not None:
        uni, created = Uni.objects.get_or_create(uni_id=request.session['uni'], defaults={'uni_name': request.session['unis'][str(request.session['uni'])]},)

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
    if request.session.get('uni') is not None:
        uni, created = Uni.objects.get_or_create(uni_id=request.session['uni'], defaults={'uni_name': request.session['unis'][str(request.session['uni'])]},)

    questions = [question for question in Question.objects.all() if question.active]
    context = {
        'message': get_message(request),
        'questions': questions,
        'unis': request.session['unis'],
    }
    return render(request, 'polls/open_polls.html', context)

def vote(request, question_id):
    if request.session.get('uni') is not None:
        uni, created = Uni.objects.get_or_create(uni_id=request.session['uni'], defaults={'uni_name': request.session['unis'][str(request.session['uni'])]},)

    question = get_object_or_404(Question, pk=question_id)
    
    if not request.session['confirmed']:
        context = {
            'message': get_message(request),
            'question': question,
            'unis': request.session['unis'],
            'error_message': "Du bist nicht stimmberechtigt",
        }
        print(context)
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', context)
    
    uni = get_object_or_404(Uni, uni_id=request.session['uni'])
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = {
            'message': get_message(request),
            'question': question,
            'unis': request.session['unis'],
            'error_message': "You didn't select a choice.",
        }
        
        # Redisplay the question voting form.
        return render(request, 'polls/vote.html', context)
    else:
        new_vote, created = Vote.objects.get_or_create(uni=uni, defaults={'choice': selected_choice})
        new_vote.choice = selected_choice
        new_vote.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results'))