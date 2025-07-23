from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
import time

from quiz.models import Country, Category, Fact


def get_client_ip(request):
    """Get client IP, considering X-Forwarded-For header"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def rate_limit_check(request):
    """Rate limit: 5 requests per second per IP"""
    client_ip = get_client_ip(request)
    cache_key = f"rate_limit_{client_ip}"
    current_time = int(time.time())
    
    # Get existing requests for this IP in current second
    requests = cache.get(cache_key, [])
    
    # Remove requests older than 1 second
    requests = [req_time for req_time in requests if current_time - req_time < 1]
    
    # Check if limit exceeded (5 requests per second)
    if len(requests) >= 5:
        return False
    
    # Add current request
    requests.append(current_time)
    cache.set(cache_key, requests, 1)
    
    return True


def serialize_fact(fact):
    """Serialize a Fact object to dict"""
    return {
        'uuid': fact.uuid,
        'answer': fact.answer,
        'notes': fact.notes,
        'image_url': fact.image_url,
        'google_streetview_url': fact.google_streetview_url,
        'google_streetview_latlng': fact.google_streetview_latlng,
        'country': {
            'name': fact.country.name,
            'slug': fact.country.slug,
            'flag_emoji': fact.country.flag_emoji(),
            'iso2': fact.country.iso2
        },
        'category': {
            'name': fact.category.name,
            'slug': fact.category.slug
        }
    }


@require_http_methods(["GET"])
@cache_page(60 * 15)  # Cache for 15 minutes
def country_metas(request, country_slug):
    """Get all metas for a specific country"""
    if not rate_limit_check(request):
        return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
    
    try:
        country = Country.objects.get(slug=country_slug)
    except Country.DoesNotExist:
        return JsonResponse({'error': 'Country not found'}, status=404)
    
    facts = Fact.objects.filter(country=country).select_related('country', 'category')
    
    return JsonResponse({
        'country': {
            'name': country.name,
            'slug': country.slug,
            'flag_emoji': country.flag_emoji(),
            'iso2': country.iso2
        },
        'metas': [serialize_fact(fact) for fact in facts],
        'total_count': len(facts)
    })


@require_http_methods(["GET"])
@cache_page(60 * 15)  # Cache for 15 minutes
def category_metas(request, category_slug):
    """Get all metas for a specific category"""
    if not rate_limit_check(request):
        return JsonResponse({'error': 'Rate limit exceeded'}, status=429)
    
    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    
    facts = Fact.objects.filter(category=category).select_related('country', 'category')
    
    return JsonResponse({
        'category': {
            'name': category.name,
            'slug': category.slug,
            'description': category.description
        },
        'metas': [serialize_fact(fact) for fact in facts],
        'total_count': len(facts)
    })