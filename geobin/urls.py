from django.contrib import admin
from django.urls import include, path

from cms.views import home
from accounts.views import accounts_login, accounts_logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include(('quiz.urls', 'quiz'), namespace='quiz')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('metas/', include(('cms.urls', 'cms'), namespace='cms')),
    path('login/', accounts_login, name='login'),
    path('logout/', accounts_logout, name='logout'),
    path('', home, name='home')
]
