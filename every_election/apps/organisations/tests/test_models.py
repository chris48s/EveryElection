from datetime import date, datetime
from django.test import TestCase
from organisations.models import Organisation, OrganisationName


class OrganisationNameTests(TestCase):

    def setUp(self):
        self.org1 = Organisation.objects.create(
            official_identifier='TEST1',
            start_date=date(2016, 10, 1),
        )

        self.org2 = Organisation.objects.create(
            official_identifier='TEST2',
            start_date=date(2016, 10, 1),
        )
        OrganisationName.objects.create(
            organisation=self.org2,
            start_date=date(2016, 10, 1),
            end_date=date(2017, 10, 1),
            slug='foo',
        )
        OrganisationName.objects.create(
            organisation=self.org2,
            start_date=date(2017, 10, 2),
            slug='bar',
        )

    def test_no_related_names(self):
        with self.assertRaises(OrganisationName.DoesNotExist):
            self.org1._get_name()

    def test_one_related_name(self):
        OrganisationName.objects.create(
            organisation=self.org1,
            start_date=date(2016, 10, 1),
            slug='foo',
        )
        name = self.org1._get_name()
        self.assertEqual('foo', name.slug)

    def test_two_related_names_no_date(self):
        with self.assertRaises(ValueError):
            self.org2._get_name()

    def test_two_related_names_invalid_dates(self):
        with self.assertRaises(Exception):
            self.org2._get_name('2019-02-31')
        with self.assertRaises(Exception):
            self.org2._get_name('foo')
        with self.assertRaises(Exception):
            self.org2._get_name(7)
        with self.assertRaises(Exception):
            self.org2._get_name(True)
        with self.assertRaises(Exception):
            self.org2._get_name([])

    def test_two_related_names_results_found(self):
        name1 = self.org2._get_name(date(2016, 12, 1))
        self.assertEqual('foo', name1.slug)
        name2 = self.org2._get_name(date(2017, 12, 1))
        self.assertEqual('bar', name2.slug)
        name3 = self.org2._get_name(datetime.today())
        self.assertEqual('bar', name3.slug)

    def test_two_related_names_no_results_found(self):
        with self.assertRaises(OrganisationName.DoesNotExist):
            self.org2._get_name(date(2001, 12, 1))
