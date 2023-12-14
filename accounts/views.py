from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.contrib.auth.models import User
from django.contrib.auth import login, logout


""" Auth0 / Authlib config """
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def accounts_login(request):
    return oauth.auth0.authorize_redirect(
        request, 
        request.build_absolute_uri(reverse("accounts:auth0_callback")),
        screen_hint='signup'
    )


def accounts_logout(request):
    # Log the user out
    logout(request)

    # Clear the session
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("accounts:auth0_logout")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


def auto0_callback(request):
    # Get the access token from Auth0
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token

    # Construct the userinfo URL
    userinfo_url = f"https://{settings.AUTH0_DOMAIN}/userinfo"

    # Get the user info from Auth0
    resp = oauth.auth0.get(userinfo_url, token=token)
    user_info = resp.json()

    # Get the email from user_info
    email = user_info.get('email')

    # Check if a user with this username or email exists
    user = User.objects.filter(username=email).first()

    # If the user does not exist, create a new user
    if not user:
        username = email
        user = User.objects.create_user(username, email)

    # Log the user in
    login(request, user)

    return redirect(request.build_absolute_uri(reverse("home")))


def auto0_logout(request):
    return redirect(request.build_absolute_uri(reverse("home")))


def profile(request):
    return render(request, "accounts/profile.html")