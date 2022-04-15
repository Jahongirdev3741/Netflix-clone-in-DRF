from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ActorViewSet,MovieAPIView,ActorAPIView,MovieActorAPIView,CommentAPIView
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register('movie',MovieViewSet,'movie')
router.register('actor',ActorViewSet,'actor')


urlpatterns = [
  path('v1/',include(router.urls)),
  path('movie/',MovieAPIView.as_view()),
  path('movie/<int:pk>/',MovieAPIView.as_view()),
  path('actor/<int:pk>/',ActorAPIView.as_view()),
  path('movie/<int:pk>/actor/',MovieActorAPIView.as_view()),
  path('comment/',CommentAPIView.as_view()),
  path('auth-token/',obtain_auth_token)
]
