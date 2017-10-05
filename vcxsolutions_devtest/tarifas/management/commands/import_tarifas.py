from django.core.management.base import BaseCommand
from openpyxl import load_workbook
from tarifas.models import Plan, SMSPlan, DataPlan


class Command(BaseCommand):
    help = 'Import data from tarifas.xlsx'

    def handle(self, *args, **options):
        self.load_data()
        self.delete_old_data()
        self.save_data()

    def _get_data_grid(self, row_range, col_range):
        return [
            [
                self._sheet['%s%d' % (y, x)].value
                for y in col_range
            ] for x in row_range
        ]

    def load_data(self):
        wb = load_workbook('tarifas/management/commands/tarifas.xlsx')
        self._sheet = wb['VC-X Solutions']

        self.plans = self._get_data_grid(
            range(4, 17), ('B', 'C', 'D', 'E', 'F')
        )
        self.sms_plans = self._get_data_grid(
            range(20, 24), ('B', 'C')
        )
        self.data_plans = self._get_data_grid(
            range(20, 24), ('E', 'F')
        )
        self.stdout.write(self.style.SUCCESS('Data loaded from sheet.'))

    def delete_old_data(self):
        Plan.objects.all().delete()
        SMSPlan.objects.all().delete()
        DataPlan.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Old data deleted.'))

    def save_data(self):
        Plan.objects.bulk_create([
            Plan(
                name=plan[0],
                minutes_franchise=plan[1],
                data_pack_unit=plan[2][-2:],
                data_pack_value=int(plan[2][:-2]),
                sms_pack_size=int(plan[3].split()[0] if plan[3] != '-' else 0),
                value=plan[4]
            )
            for plan in self.plans
        ])
        self.stdout.write(self.style.SUCCESS('Plans saved.'))

        SMSPlan.objects.bulk_create([
            SMSPlan(
                sms_pack_size=(
                    int(plan[0].split()[0]) if plan[0][0] != 'S' else None
                ),
                value=plan[1]
            )
            for plan in self.sms_plans
        ])
        self.stdout.write(self.style.SUCCESS('SMS Plans saved.'))

        DataPlan.objects.bulk_create([
            Plan(
                data_pack_unit=plan[0][-2:],
                data_pack_value=int(plan[0][:-3]),
                value=plan[1]
            )
            for plan in self.data_plans
        ])
        self.stdout.write(self.style.SUCCESS('Data Plans saved.'))
