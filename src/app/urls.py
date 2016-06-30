from .views.api import ApiDescription, GenreResourceView

URLS = (
    ('/', ApiDescription, 'api_description'),
    ('/genres', GenreResourceView, 'genres'),

)
