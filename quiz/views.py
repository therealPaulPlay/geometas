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
    try:
        # Check if there's an existing quiz of this type & user in progress
        quiz_session = QuizSession.objects.get(
            user=request.user,
            quiz=quiz,
            state="in_progress"
        )
    except QuizSession.DoesNotExist:
        # Mark old in_progress sessions as cancelled
        old_sessions = QuizSession.objects.filter(
            user=request.user,
            state="in_progress"
        )
        for old_session in old_sessions:
            old_session.mark_cancelled()
        
        # Create new session
        quiz_session = QuizSession.objects.create(
            user=request.user,
            quiz=quiz,
            state="in_progress"
        )
        log.info(f"Created new session {quiz_session.uuid}")
        quiz_session.load_facts()

        
    
    # Get first fact
    first_session_fact = QuizSessionFact.objects.filter(
        quiz=quiz,
        quiz_session=quiz_session,
        user=request.user,
        review_result__isnull=True
    ).order_by('sort_order').first()

    # Redirect to summary page if no facts left
    if not first_session_fact:
        quiz_session.state = "finished"
        quiz_session.save()
        return redirect('quiz:summary', quiz_uuid=quiz.uuid, quiz_session_uuid=quiz_session.uuid)
    
    return redirect('quiz:question', quiz_uuid=quiz_uuid, fact_uuid=first_session_fact.fact.uuid)


@login_required
def question(request, quiz_uuid, fact_uuid):
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    fact = Fact.objects.get(uuid=fact_uuid)
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz=quiz,
        quiz_session__user=request.user,
        quiz_session__state="in_progress",
        fact=fact
    )
    context = {
        'fact': fact,
        'quiz': quiz,
        'quiz_session_fact': quiz_session_fact,
        'progress_pct': round((quiz_session_fact.sort_order-1) / quiz.num_facts_user_facing * 100, 0),
        'html_meta_title': "%s - Question %s / %s" % (quiz.name, quiz_session_fact.sort_order, quiz.num_facts_user_facing),
        'html_meta_description': "Take the quiz '%s' on Geometas to become a Geoguessr champion" % quiz.name,
        # 'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'quiz/question.html', context)


@login_required
def answer(request, quiz_uuid, fact_uuid):
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    fact = Fact.objects.get(uuid=fact_uuid)
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz=quiz,
        quiz_session__user=request.user,
        quiz_session__state="in_progress",
        fact=fact
    )

    context = {
        'fact': fact,
        'quiz': quiz,
        'quiz_session_fact': quiz_session_fact,
        'progress_pct': round((quiz_session_fact.sort_order-1) / quiz.num_facts_user_facing * 100, 0),
        'html_meta_title': "%s - Answer %s / %s" % (quiz.name, quiz_session_fact.sort_order, quiz.num_facts_user_facing),
        'html_meta_description': "Take the quiz '%s' on Geometas to become a Geoguessr champion" % quiz.name,
        # 'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'quiz/answer.html', context)


@login_required
def rate_fact(request, quiz_uuid, fact_uuid):
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    fact = Fact.objects.get(uuid=fact_uuid)

    # Get rating from URL param
    # Should be 'correct' or 'false'
    rating = request.GET.get('r', None)
    if rating not in ['correct', 'false']:
        raise Exception("Invalid rating")

    # Get this Quiz Session Fact and set review result
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz=quiz,
        quiz_session__user=request.user,
        quiz_session__state="in_progress",
        fact=fact
    )
    if rating == 'correct':
        quiz_session_fact.set_correct()
        log.info(f"User {request.user.username} rated fact {fact.uuid} as correct")
    elif rating == 'false':
        quiz_session_fact.set_false()
        log.info(f"User {request.user.username} rated fact {fact.uuid} as false")

    # Redirect to quiz 
    return redirect('quiz:quiz', quiz_uuid=quiz_uuid)


@login_required
def summary(request, quiz_uuid, quiz_session_uuid):
    quiz_session = QuizSession.objects.get(uuid=quiz_session_uuid)
    # Calculate the total number of quizsessionfacts, how many are correct and how many are false
    total_fact_count = quiz_session.quiz.num_facts_user_facing
    correct_fact_count = quiz_session.quizsessionfacts.filter(review_result="correct").count() or 0
    correct_percentage = round(correct_fact_count / total_fact_count * 100, 0)
    context = {
        'session': quiz_session,
        'total_fact_count': total_fact_count,
        'correct_fact_count': correct_fact_count,
        'correct_percentage': correct_percentage,
        'html_meta_title': "%s - Summary" % quiz_session.quiz.name,
        'html_meta_description': "Take the quiz '%s' on Geometas to become a Geoguessr champion" % quiz_session.quiz.name,
        # 'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'quiz/summary.html', context)
