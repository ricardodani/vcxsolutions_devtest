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

    @staticmethod
    def _parse_data_mb(data_plan):
        int_part, unit_part = int(data_plan[:-2]), data_plan[-2:]
        return int_part if unit_part == 'MB' else int_part * 1024

    @staticmethod
    def _parse_sms_pack_size(sms_pack):
        if sms_pack == '-':
            return 0
        else:
            return int(sms_pack.split()[0])

    @staticmethod
    def _parse_sms_pack_size_2(sms_pack):
        return int(sms_pack.split()[0]) if sms_pack[0] != 'S' else None

    def save_data(self):
        Plan.objects.bulk_create([
            Plan(
                name=plan[0],
                minutes_franchise=plan[1],
                data_mb=self._parse_data_mb(plan[2]),
                data_unit=plan[2][-2:],
                sms_pack_size=self._parse_sms_pack_size(plan[3]),
                value=plan[4]
            )
            for plan in self.plans
        ])
        self.stdout.write(self.style.SUCCESS('Plans saved.'))

        SMSPlan.objects.bulk_create([
            SMSPlan(
                sms_pack_size=self._parse_sms_pack_size_2(plan[0]),
                value=plan[1]
            )
            for plan in self.sms_plans
        ])
        self.stdout.write(self.style.SUCCESS('SMS Plans saved.'))

        DataPlan.objects.bulk_create([
            Plan(
                data_mb=self._parse_data_mb(plan[0]),
                data_unit=plan[0][-2:],
                value=plan[1]
            )
            for plan in self.data_plans
        ])
        self.stdout.write(self.style.SUCCESS('Data Plans saved.'))
