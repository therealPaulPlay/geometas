from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
import logging
log = logging.getLogger(__name__)

from .models import Fact, Quiz, QuizSession, QuizSessionFact


@login_required
def quiz(request, quiz_uuid):
    # Retrieve Quiz
    quiz = Quiz.objects.get(uuid=quiz_uuid)

    # Get or create Quiz Session
    quiz_session, created = QuizSession.objects.get_or_create(
        user=request.user,
        quiz=quiz,
        state="in_progress"
    )
    if created:
        log.info(f"Created new session {quiz_session.uuid}")
        quiz_session.load_facts()

        # Mark old in_progress sessions as cancelled
        old_sessions = QuizSession.objects.filter(
            user=request.user,
            quiz=quiz,
            state="in_progress"
        ).exclude(uuid=quiz_session.uuid)
        for old_session in old_sessions:
            old_session.state = "cancelled"
            old_session.save()
            log.info(f"Cancelled old session {old_session.uuid}")
    
    # Get first fact
    first_session_fact = QuizSessionFact.objects.filter(
        quiz=quiz,
        quiz_session=quiz_session,
        user=request.user,
        review_result__isnull=True
    ).order_by('sort_order').first()

    # Redirect to home if no facts left
    if not first_session_fact:
        raise Exception("No facts left")
    
    return redirect('quiz:question', quiz_uuid=quiz_uuid, fact_uuid=first_session_fact.fact.uuid)


@login_required
def question(request, quiz_uuid, fact_uuid):
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    fact = Fact.objects.get(uuid=fact_uuid)
    context = {
        'fact': fact,
        'quiz': quiz
    }
    return render(request, 'quiz/question.html', context)


@login_required
def answer(request, quiz_uuid, fact_uuid):
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    fact = Fact.objects.get(uuid=fact_uuid)

    # Get this Quiz Session Fact and set review result
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz=quiz,
        quiz_session__user=request.user,
        quiz_session__quiz=quiz,
        fact=fact
    )
    quiz_session_fact.review_result = "not_set"
    quiz_session_fact.save()

    # Check if this is the last fact in the quiz session
    quiz_session = QuizSession.objects.get(
        user=request.user,
        quiz=quiz,
        state="in_progress"
    )
    quiz_session_fact = QuizSessionFact.objects.filter(
        quiz=quiz,
        quiz_session=quiz_session,
        user=request.user,
        review_result__isnull=True
    )
    if quiz_session_fact.count() == 1:
        quiz_session.state = "finished"
        quiz_session.save()

    context = {
        'fact': fact,
        'quiz': quiz,
        'quiz_finished': (quiz_session.state == "finished")
    }
    return render(request, 'quiz/answer.html', context)


@login_required
def home(request):
    quizzes_by_meta = Quiz.objects.filter(category__isnull=False)
    quizzes_by_country = Quiz.objects.filter(category__isnull=True)
    # Get in_progress quiz session of this user
    try:
        quiz_session = QuizSession.objects.get(
            user=request.user,
            state="in_progress"
        )
    except QuizSession.DoesNotExist:
        quiz_session = None
    context = {
        'quizzes_by_meta': quizzes_by_meta,
        'quizzes_by_country': quizzes_by_country,
        'quiz_session': quiz_session
    }
    return render(request, 'quiz/home.html', context)