from tests.factory import Factory
from pgsqlutils.orm import Session


def run(**kwargs):
    factory = Factory(Session)

    print("Generating sample data:")

    # artist data
    print("artists...")
    factory.clear_artists()
    factory.get_artist()

    print("Sample db population complete...")
