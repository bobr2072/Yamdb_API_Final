from api.views import CommentViewSet, ReviewViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, register, token

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

VERSION = 'v1'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path(f'{VERSION}/', include(router_v1.urls)),
    path(f'{VERSION}/auth/signup/', register, name='register'),
    path(f'{VERSION}/auth/token/', token, name='login'),
]
