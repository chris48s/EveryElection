from django.core.management.base import BaseCommand
from organisations.models import Organisation, OrganisationDivisionSet
from core.mixins import ReadFromCSVMixin


class Command(ReadFromCSVMixin, BaseCommand):

    def handle(self, *args, **options):
        print("records with default start date: %s" %
            len(Organisation.objects.all().filter(start_date='2016-10-01'))
        )

        csv_data = self.load_csv_data(options)
        for row in csv_data:
            org = Organisation.objects.all().get(
                official_identifier=row['official_identifier'],
                organisation_type=row['organisation_type']
            )

            if row['start_date'] == 'deleteme':
                org.delete()
            else:
                org.start_date = row['start_date']
                org.save()

        print("records with default start date: %s" %
            len(Organisation.objects.all().filter(start_date='2016-10-01'))
        )

        sets = OrganisationDivisionSet.objects.all().order_by('start_date')
        print("Checking %i Division Sets..." % (len(sets)))
        for ods in sets:
            if ods.start_date < ods.organisation.start_date:
                print("ODS '%s' has start date before org '%s'! :(" % (ods, ods.organisation))
