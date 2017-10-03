from django.db import models


class Plan(models.Model):
    '''Plano'''

    name = models.CharField(
        verbose_name='Nome do Plano',
        max_length=15
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
    data_pack.fget.short_description = 'Pacote de dados'

    sms_pack_size = models.IntegerField(
        verbose_name='Pacote de SMS',
        default=0,
    )

    @property
    def sms_pack(self):
        if self.sms_pack_size > 0:
            return '{} SMS'.format(self.sms_pack_size)
        else:
            return '-'
    sms_pack.fget.short_description = 'Pacote de SMS'

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
        max_digits=8
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Plano'


class SMSPlan(models.Model):
    '''Plano de SMS Adicional'''

    sms_pack_size = models.PositiveIntegerField(
        verbose_name='Pacote de SMS',
        null=True,
        blank=True
    )

    @property
    def sms_pack(self):
        if self.sms_pack_size:
            return '{} SMS'.format(self.sms_pack_size)
        else:
            return 'SMS ILIMITADOS'
    sms_pack.fget.short_description = 'Pacote de SMS Adicional'

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
        max_digits=8
    )

    def __str__(self):
        return self.sms_pack

    class Meta:
        verbose_name = 'Plano de SMS Adicional'
        verbose_name_plural = 'Planos de SMS Adicionais'


class DataPlan(models.Model):
    '''Plano de Dados Adicional'''

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
    data_pack.fget.short_description = 'Pacote de dados Adicional'

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
        max_digits=8
    )

    def __str__(self):
        return self.data_pack

    class Meta:
        verbose_name = 'Plano de Dados Adicional'
