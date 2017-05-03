from .views.api import ApiDescription, GenreResourceView, ArtistResourceView

URLS = (
    ('/', ApiDescription, 'api_description'),
    ('/genres', GenreResourceView, 'genres'),
    ('/artists', ArtistResourceView, 'artists'),
    ('/artists/<uuid:uuid>', ArtistResourceView, 'specific_artist'),
)
