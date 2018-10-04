import datetime
import factory

from elections.models import (
    Election,
    ElectionModerationStatus,
    ElectionType,
    ElectedRole,
    ModerationStatus
)
from organisations.tests.factories import (
    OrganisationFactory,
    OrganisationDivisionFactory,
    DivisionGeographyFactory
)


class ElectionTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ElectionType
        django_get_or_create = ('election_type', )

    name = "Local elections"
    election_type = "local"
    # default_voting_system


class ElectedRoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ElectedRole
        django_get_or_create = ('election_type', )

    election_type = factory.SubFactory(ElectionTypeFactory)
    organisation = factory.SubFactory(OrganisationFactory)
    elected_title = "Councillor"
    elected_role_name = "Councillor"


class ElectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Election
        django_get_or_create = ('election_id', )

    @classmethod
    def _get_manager(cls, model_class):
        return model_class.private_objects

    election_id = factory.Sequence(
        lambda n: 'local.place-name-%d.2017-03-23' % n)
    election_title = factory.Sequence(lambda n: 'Election %d' % n)
    election_type = factory.SubFactory(ElectionTypeFactory)
    poll_open_date = "2017-03-23"
    organisation = factory.SubFactory(OrganisationFactory)
    elected_role = factory.SubFactory(ElectedRoleFactory)
    division = factory.SubFactory(OrganisationDivisionFactory)
    division_geography = factory.SubFactory(DivisionGeographyFactory)
    organisation_geography = None
    seats_contested = 1
    seats_total = 1
    group = factory.SubFactory(
        'elections.tests.factories.ElectionFactory',
        election_id="local.2017-03-23",
        group=None, group_type="election")
    group_type = None


class ModerationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ModerationStatus
        django_get_or_create = ('short_title', )
    short_title = 'Approved'
    long_title = 'long title'


class ElectionModerationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ElectionModerationStatus

    election = factory.SubFactory(ElectionFactory)
    status = factory.SubFactory(ModerationStatusFactory)
    created = datetime.datetime.now()
    modified = datetime.datetime.now()


def create_election_with_status(*args, **kwargs):
    try:
        status = kwargs.pop('moderation_status')
    except KeyError:
        status = 'Approved'
    election = ElectionFactory(*args, **kwargs)
    ElectionModerationStatusFactory(
        election=election,
        status=ModerationStatusFactory(short_title=status)
    )
    return election
