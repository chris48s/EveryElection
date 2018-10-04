from datetime import datetime, timedelta

from django.test import TestCase
from django.contrib.gis.geos import Point

from elections.tests.factories import (
    create_election_with_status,
    ElectionFactory,
    ElectionModerationStatusFactory,
    ModerationStatusFactory,
)
from elections.models import Election


class TestElectionGeoQueries(TestCase):
    lat = 51.5010089365
    lon = -0.141587600123

    fixtures = ['onspd.json']

    def test_election_for_point(self):
        create_election_with_status(group=None)
        point = Point(self.lon, self.lat)
        qs = Election.public_objects.for_point(point)
        assert qs.count() == 1

    def test_election_for_lat_lng(self):
        create_election_with_status(group=None)
        qs = Election.public_objects.for_lat_lng(
            lat=self.lat, lng=self.lon)
        assert qs.count() == 1

    def test_election_for_postcode(self):
        create_election_with_status(group=None)
        qs = Election.public_objects.for_postcode("SW1A 1AA")
        assert qs.count() == 1

    def test_current_elections(self):
        # This is implicetly current
        create_election_with_status(group=None, poll_open_date=datetime.today())
        # This is implicetly not current
        create_election_with_status(
            group=None, poll_open_date=datetime.today() - timedelta(days=60))
        # This is implicetly not current, but current manually set
        create_election_with_status(
            group=None,
            poll_open_date=datetime.today() - timedelta(days=60),
            current = True
            )
        # This is implicetly current, current manually set to False
        create_election_with_status(
            group=None,
            poll_open_date=datetime.today() - timedelta(days=1),
            current = False
            )
        assert Election.public_objects.current().count() == 2

    def test_future_elections(self):
        create_election_with_status(group=None, poll_open_date=datetime.today())
        create_election_with_status(
            group=None, poll_open_date=datetime.today() - timedelta(days=1))
        assert Election.public_objects.future().count() == 1

    def test_current_elections_for_postcode(self):
        create_election_with_status(group=None, poll_open_date=datetime.today())
        create_election_with_status(
            group=None, poll_open_date=datetime.today(), division_geography=None)
        create_election_with_status(
            group=None, poll_open_date=datetime.today() - timedelta(days=60) )
        assert Election.public_objects.current().for_postcode('SW1A1AA').count() == 1

    def test_public_private_filter_simple(self):
        # simple case: each election only has a single status event
        create_election_with_status(group=None, moderation_status='Suggested')
        create_election_with_status(group=None, moderation_status='Approved')
        create_election_with_status(group=None, moderation_status='Rejected')
        create_election_with_status(group=None, moderation_status='Deleted')
        self.assertEqual(1, Election.public_objects.count())
        self.assertEqual(4, Election.private_objects.count())

    def test_public_private_filter_complex(self):
        # set up 2 ballot objects
        e1 = ElectionFactory(group=None)
        e2 = ElectionFactory(group=None)

        # to start off with they're both 'suggested'
        ElectionModerationStatusFactory(
            election=e1,
            status=ModerationStatusFactory(short_title='Suggested')
        )
        ElectionModerationStatusFactory(
            election=e2,
            status=ModerationStatusFactory(short_title='Suggested')
        )
        self.assertEqual(0, Election.public_objects.count())
        self.assertEqual(2, Election.private_objects.count())

        # approve one of them
        ElectionModerationStatusFactory(
            election=e1,
            status=ModerationStatusFactory(short_title='Approved')
        )
        self.assertEqual(1, Election.public_objects.count())
        self.assertEqual(
            e1.election_id, Election.public_objects.all()[0].election_id)
        self.assertEqual(2, Election.private_objects.count())

        # and then delete it again
        ElectionModerationStatusFactory(
            election=e1,
            status=ModerationStatusFactory(short_title='Deleted')
        )
        self.assertEqual(0, Election.public_objects.count())
        self.assertEqual(2, Election.private_objects.count())
