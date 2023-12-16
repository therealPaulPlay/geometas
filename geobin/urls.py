from django.contrib import admin
from django.urls import include, path

from quiz.views import quiz_index
from accounts.views import accounts_login, accounts_logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('login/', accounts_login, name='login'),
    path('logout/', accounts_logout, name='logout'),
    path('', quiz_index, name='home')
]
