from .views.api import ApiDescription, ArtistResourceView

URLS = (
    ('/', ApiDescription, 'api_description'),
    ('/artists', ArtistResourceView, 'artists'),
    ('/artists/<uuid:uuid>', ArtistResourceView, 'specific_artist'),
)
