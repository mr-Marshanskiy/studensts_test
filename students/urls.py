from django.urls import include, path
from rest_framework.routers import DefaultRouter

from students.views import sections, dicts, members, students

router = DefaultRouter()

router.register(r'students', students.StudentView, 'students')
router.register(r'sections/dicts/directions', dicts.DirectionView, 'directions')
router.register(r'sections/(?P<pk>\d+)/members', members.MemberView, 'members')
router.register(r'sections/', sections.SectionView, 'sections')

urlpatterns = [
    path('', include(router.urls)),
]