from django.urls import include, path

from api.spectacular.urls import urlpatterns as doc_urls
from students.urls import urlpatterns as student_urls
from users.urls import urlpatterns as user_urls

app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += student_urls
urlpatterns += user_urls
