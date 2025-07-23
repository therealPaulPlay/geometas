from django.shortcuts import render, redirect
from django.http import Http404
import logging
log = logging.getLogger(__name__)

from .models import Fact, Quiz, QuizSession, QuizSessionFact


def start_quiz(request, quiz_uuid):
    # Retrieve Quiz
    quiz = Quiz.objects.get(uuid=quiz_uuid)

    # Create Quiz Session
    # Mark old in_progress sessions as cancelled if user is logged in
    if request.user.is_authenticated:
        old_sessions = QuizSession.objects.filter(
            user=request.user,
            state="in_progress"
        )
        for old_session in old_sessions:
            old_session.mark_cancelled()
    
    # Create new session
    quiz_session = QuizSession.objects.create(
        user=request.user if request.user.is_authenticated else None,
        quiz=quiz
    )
    log.info(f"Created new session {quiz_session.uuid}")
    quiz_session.load_facts()

    # Get first fact
    first_session_fact = quiz_session.get_next_fact()
    if not first_session_fact:
        raise Exception("No facts found for newly started quiz session")
    
    return redirect('quiz:question', quiz_session_uuid=quiz_session.uuid, fact_uuid=first_session_fact.fact.uuid)


def continue_quiz(request, quiz_session_uuid):
    try:
        quiz_session = QuizSession.objects.select_related('quiz').get(uuid=quiz_session_uuid, user_id=request.user.id)
    except QuizSession.DoesNotExist:
        raise Http404("Quiz session does not exist for this user")
    next_quiz_session_fact = quiz_session.get_next_fact()
    
    # If no facts left then mark finished and redirect to summary page 
    if not next_quiz_session_fact:
        quiz_session.mark_finished()
        return redirect('quiz:summary', quiz_session_uuid=quiz_session.uuid)
    
    # Redirect to next question
    return redirect('quiz:question', quiz_session_uuid=quiz_session.uuid, fact_uuid=next_quiz_session_fact.fact.uuid)
    

def question(request, quiz_session_uuid, fact_uuid):
    try:
        quiz_session = QuizSession.objects.select_related('quiz').get(uuid=quiz_session_uuid, user_id=request.user.id)
    except QuizSession.DoesNotExist:
        raise Http404("Quiz session does not exist for this user")
    fact = Fact.objects.get(uuid=fact_uuid)
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz_session=quiz_session,
        fact=fact
    )
    context = {
        'fact': fact,
        'quiz_session': quiz_session,
        'quiz_session_fact': quiz_session_fact,
        'progress_pct': round((quiz_session_fact.sort_order-1) / quiz_session.num_questions * 100, 0),
        'html_meta_title': "%s - Question %s / %s" % (quiz_session.quiz.name, quiz_session_fact.sort_order, quiz_session.num_questions),
        'html_meta_description': "Take the quiz '%s' on Geometas to become a GeoGuessr champion" % quiz_session.quiz.name,
        # 'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'quiz/question.html', context)


def answer(request, quiz_session_uuid, fact_uuid):
    try:
        quiz_session = QuizSession.objects.select_related('quiz').get(uuid=quiz_session_uuid, user_id=request.user.id)
    except QuizSession.DoesNotExist:
        raise Http404("Quiz session does not exist for this user")
    fact = Fact.objects.get(uuid=fact_uuid)
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz_session=quiz_session,
        fact=fact
    )

    context = {
        'fact': fact,
        'quiz_session': quiz_session,
        'quiz_session_fact': quiz_session_fact,
        'progress_pct': round((quiz_session_fact.sort_order-1) / quiz_session.num_questions * 100, 0),
        'html_meta_title': "%s - Answer %s / %s" % (quiz_session.quiz.name, quiz_session_fact.sort_order, quiz_session.num_questions),
        'html_meta_description': "Take the quiz '%s' on Geometas to become a GeoGuessr champion" % quiz_session.quiz.name,
        # 'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'quiz/answer.html', context)


def rate_fact(request, quiz_session_uuid, fact_uuid):
    try:
        quiz_session = QuizSession.objects.select_related('quiz').get(uuid=quiz_session_uuid, user_id=request.user.id)
    except QuizSession.DoesNotExist:
        raise Http404("Quiz session does not exist for this user")
    fact = Fact.objects.get(uuid=fact_uuid)

    # Get rating from URL param
    # Should be 'correct' or 'false'
    rating = request.GET.get('r', None)
    if rating not in ['correct', 'false']:
        log.warning("User %s tried to rate fact %s with invalid rating %s" % (request.user, fact, rating))
        raise Http404("Invalid rating")

    # Get this Quiz Session Fact and set review result
    quiz_session_fact = QuizSessionFact.objects.get(
        quiz_session=quiz_session,
        fact=fact
    )
    if rating == 'correct':
        quiz_session_fact.set_correct()
        log.info(f"User {request.user.username} rated fact {fact.uuid} as correct")
    elif rating == 'false':
        quiz_session_fact.set_false()
        log.info(f"User {request.user.username} rated fact {fact.uuid} as false")

    # Redirect to quiz 
    return redirect('quiz:continue_quiz', quiz_session_uuid=quiz_session.uuid)


def summary(request, quiz_session_uuid):
    try:
        quiz_session = QuizSession.objects.select_related('quiz').get(uuid=quiz_session_uuid, user_id=request.user.id)
    except QuizSession.DoesNotExist:
        raise Http404("Quiz session does not exist for this user")
    # Calculate the total number of quizsessionfacts, how many are correct and how many are false
    total_fact_count = quiz_session.num_questions
    correct_fact_count = quiz_session.quizsessionfacts.filter(review_result="correct").count() or 0
    correct_percentage = round(correct_fact_count / total_fact_count * 100, 0)
    context = {
        'session': quiz_session,
        'total_fact_count': total_fact_count,
        'correct_fact_count': correct_fact_count,
        'correct_percentage': correct_percentage,
        'html_meta_title': "%s - Summary" % quiz_session.quiz.name,
        'html_meta_description': "Take the quiz '%s' on Geometas to become a GeoGuessr champion" % quiz_session.quiz.name,
        # 'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'quiz/summary.html', context)
