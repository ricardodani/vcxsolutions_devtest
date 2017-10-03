from django.db import models


class Plan(models.Model):
    '''Plano'''

    name = models.CharField(
        verbose_name='Nome do Plano',
        max_lenght=15
    )

    minutes_franchise = models.IntegerField(
        verbose_name='Franquia de Minutos',
        default=0
    )

    data_pack_unit = models.CharField(
        verbose_name='Pacote de dados (unidade)',
        choices=(('MB', 'Megabyte'), ('GB', 'Gigabyte')),
        max_length=2
    )

    data_pack_value = models.PositiveIntegerField(
        verbose_name='Pacote de dados (valor)',
    )

    @property
    def data_pack(self):
        return '{}{}'.format(self.data_pack_value, self.data_pack_unit)
    data_pack.verbose_name = 'Pacote de dados'

    sms_pack_size = models.PositiveIntegerField(
        verbose_name='Pacote de SMS',
    )

    @property
    def sms_pack(self):
        return '{} SMS'.format(self.sms_pack_size)
    sms_pack.verbose_name = 'Pacote de SMS'

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Plano'
