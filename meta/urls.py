from django.urls import path
from . import views

def extra(model, field):
    return {'model_name': model, 'field': field}

urlpatterns = [
        path('', views.home_page, name='home'),

        # Menu
        path('search/', views.search_page, name='search_url'),
        path('organization/', views.org_page, name='org_url'),
        path('tags/', views.tags_page, name='tags_url'),
        path('taxa/', views.taxa_page, name='taxa_url'),
        path('places/', views.places_page, name='places_url'),
        path('authors/', views.authors_page, name='persons_url'),
        path('literature/', views.refs_page, name='refs_url'),
        path('tours/', views.tours_page, name='tours_url'),
        path('press/', views.press_page, name='press_url'),

        # Media pages
        path('tour/<slug:slug>/', views.tour_page, name='tour_url'),
        path('media/<int:media_id>/', views.media_page, name='media_url'),
        path('photo/<int:old_id>/', views.old_media, {'datatype':'image'}),
        path('video/<int:old_id>/', views.old_media, {'datatype': 'video'}),

        # Meta pages
        path('tag/<slug:slug>/', views.search_page, extra('Tag', 'tag'),
            name='tag_url'),
        path('author/<slug:slug>/', views.search_page, extra('Person',
            'author'), name='person_url'),
        path('taxon/<slug:slug>/', views.search_page, extra('Taxon', 'taxon'),
            name='taxon_url'),
        path('place/<slug:slug>/', views.search_page, extra('Location',
            'location'), name='location_url'),
        path('city/<slug:slug>/', views.search_page, extra('City', 'city'),
            name='city_url'),
        path('state/<slug:slug>/', views.search_page, extra('State', 'state'),
            name='state_url'),
        path('country/<slug:slug>/', views.search_page, extra('Country',
            'country'), name='country_url'),
        path('reference/<slug:slug>/', views.search_page, extra('Reference',
            'reference'), name='reference_url'),
        ]
