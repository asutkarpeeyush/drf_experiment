from django.urls import path, re_path
from django.conf.urls import include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

# build views from view sets
# people_view = views.PersonViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# person_view = views.PersonViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# Router for person urls
drf_router = DefaultRouter()
drf_router.register(r'details', views.PersonViewSet)

urlpatterns = [
    # function based
    # path('details', views.people_details, name='drf_people_details'),
    # path('details/<int:person_id>', views.person_details,
    #      name='drf_person_details'),

    # class based
    # path('details', views.PeopleDetails.as_view(), name='drf_people_details'),
    # path('details/<int:person_id>', views.PersonDetails.as_view(),
    #      name='drf_person_details'),

    # class based with mixin
    # path('details', views.PeopleDetailsUsingMixin.as_view(),
    #      name='drf_people_details'),
    # path('details/<person>', views.PersonDetailsUsingMixin.as_view(),
    #      name='drf_person_details'),

    # class based with generic views
    # path('details', views.PeopleDetailsUsingGenerics.as_view(),
    #      name='drf_people_details'),
    # path('details/<person>', views.PersonDetailsUsingGenerics.as_view(),
    #      name='drf_person_details'),

    # url conf using view sets
    # path('details', people_view, name='drf_people_details'),
    # path('details/<person>', person_view, name='drf_person_details'),

    # url conf using routers
    path('v1/', include((drf_router.urls, 'drf'), namespace='v1')),
    path('v2/', include((drf_router.urls, 'drf'), namespace='v2'))
]

# urlpatterns = format_suffix_patterns(urlpatterns)
