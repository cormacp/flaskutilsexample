from tests.factory import Factory
from pgsqlutils.orm import Session


def run(**kwargs):
    factory = Factory(Session)

    # artist data
    factory.clear_artists()
    factory.get_artist()

    # # chord data
    # factory.clear_chords()
    # factory.create_chords()
    #
    # # song data
    # factory.clear_songs()
    # factory.create_songs()
    #
    # # songfeed data
    # factory.clear_songfeeds()
    # factory.create_songfeeds()
