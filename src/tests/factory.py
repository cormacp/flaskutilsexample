from app.models import Genre, Artist
import uuid
import random
import string


class Factory(object):
    def __init__(self, PGSession):
        self.PGSession = PGSession

    @classmethod
    def create_unique_string(cls, prefix='', n_range=6):
        st = ''.join(
            random.choice(
                string.ascii_lowercase + string.digits)
            for x in range(n_range))

        if prefix:
            return '{0}-{1}'.format(prefix, st)
        else:
            return '{0}'.format(st)

    # def get_random_word_list(self, n=50):
    #     return ' '.join([self.create_unique_string() for x in range(n)])
    #
    # def get_random_time_series(self, n=50):
    #     def get_number(i):
    #         return i + random.uniform(0, 1)
    #
    #     return [get_number(i) for i in range(50)]

    # def get_random_chord(self):
    #     EXISTING_CHORDS = (
    #         'A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',
    #         'Am', 'A#m', 'Bm', 'Cm', 'C#m', 'Dm', 'D#m', 'Em', 'Fm', 'F#m',
    #         'Gm', 'G#m'
    #     )
    #     return random.choice(EXISTING_CHORDS)
    #
    # def get_random_chord_list(self, n=50):
    #     return [self.get_random_chord() for x in range(n)]

    def get_artist(self, **kwargs):
            string = self.create_unique_string()
            properties = {
                'key': uuid.uuid4(),
                'name': string,
                'image': 'http://www.imageurl.com/image.jpeg',
                'members': [],
                'related_artists': [],
                'is_popular': 'True',
                'first_character': string[0]
            }

            for k, v in kwargs.items():
                properties[k] = v

            if 'related_artists' in properties:
                properties['related_artists'] =\
                    list(map(str, properties['related_artists']))
            obj = Artist(**properties)
            obj.add()
            self.PGSession.commit()
            return obj

    def clear_artists(self):
        for artist_item in Artist.objects.filter_by():
            artist_item.delete()
        return self.PGSession.commit()
