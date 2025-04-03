from .common import InfoExtractor
from ..utils import (
    clean_podcast_url,
    float_or_none,
    int_or_none,
    parse_iso8601,
)
from ..utils.traversal import traverse_obj


class OmnyFMIE(InfoExtractor):
    _VALID_URL = r'https?://omny\.fm/shows/(?P<show>[^/]+)/(?P<clip>[^/?#]+)'
    _TESTS = [
        {
            'url': 'https://omny.fm/shows/behind-the-bastards/part-two-the-grifters-behind-the-fake-autism-cure-industry',
            'md5': '8076ed253415583770045b00df49c3a8',
            'info_dict': {
                'id': '97434dbc-b31c-4a2c-8172-b2b40033871d',
                'display_id': 'part-two-the-grifters-behind-the-fake-autism-cure-industry',
                'series': 'Behind the Bastards',
                'series_id': 'e5f91208-cc7e-4726-a312-ae280140ad11',
                'ext': 'mp3',
                'title': "Part Two: The Grifters Behind The Fake Autism 'Cure' Industry",
                'description': 'md5:483c5405b749e7a688f23add9f09bbf6',
                'upload_date': '20250403',
                'timestamp': 1743670800,
                'duration': 3289.428,
                'thumbnail': 're:.+[.](png|jpe?g|webp)',
            },
        },
        {
            'url': 'https://omny.fm/shows/l-haut-sur-la-colline-antoine-robitaille/le-ministre-mal-aim-ric-caire-en-lutte-contre-sa-m',
            'md5': 'ac5e9017a709116e74598191d0997ce1',
            'info_dict': {
                'id': '1b8be429-08d4-42c3-a9ba-b18f0134a082',
                'display_id': 'le-ministre-mal-aim-ric-caire-en-lutte-contre-sa-m',
                'series': 'Antoine Robitaille',
                'series_id': 'e5098503-b4ab-4036-882b-a96f0003a14f',
                'ext': 'mp3',
                'title': 'Le ministre mal-aimé Éric Caire en lutte contre sa mauvaise réputation',
                'description': 'md5:9c3d7b60af18b7dd298755d79a3ac65a',
                'upload_date': '20240614',
                'timestamp': 1718390904,
                'duration': 1687.641,
                'thumbnail': 're:.+[.](png|jpe?g|webp)',
            },
        },
    ]

    def _real_extract(self, url):
        show_slug, clip_slug = self._match_valid_url(url).group('show', 'clip')
        api_url = f'https://api.omny.fm/programs/{show_slug}/clips/{clip_slug}?includeProgramDetail=true'
        clip_data = self._download_json(api_url, clip_slug)

        return {
            'id': clip_data['Id'],
            'display_id': clip_slug,
            'vcodec': 'none',
            **traverse_obj(
                clip_data,
                {
                    'title': ('Title', {str}),
                    'url': ('AudioUrl', {clean_podcast_url}),
                    'timestamp': ('PublishedUtc', {parse_iso8601}),
                    'description': ('Description', {str}),
                    'duration': ('DurationSeconds', {float_or_none}),
                    'thumbnail': ('ImageUrl', {str}),
                    'series': ('Program', 'Name', {str}),
                    'series_id': ('Program', 'Id', {str}),
                    'episode_number': ('Episode', {int_or_none}),
                    'season_number': ('Season', {int_or_none}),
                },
            ),
        }
