from app.models import Artist
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
