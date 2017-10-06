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

    data_mb = models.IntegerField(
        verbose_name='Pacote de dados (MB)',
    )

    data_unit = models.CharField(
        verbose_name='Pacote de dados (unidade)',
        choices=(('MB', 'Megabyte'), ('GB', 'Gigabyte')),
        max_length=2
    )

    sms_pack_size = models.IntegerField(
        verbose_name='Pacote de SMS',
        default=0,
    )

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
        max_digits=8
    )

    @property
    def data_display(self):
        if self.data_unit == 'MB':
            return '{}MB'.format(self.data_mb)
        else:
            return '{}GB'.format(self.data_mb // 1024)
    data_display.fget.short_description = 'Pacote de dados'

    @property
    def sms_pack(self):
        if self.sms_pack_size > 0:
            return '{} SMS'.format(self.sms_pack_size)
        else:
            return '-'
    sms_pack.fget.short_description = 'Pacote de SMS'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Plano'
        ordering = ['name']


class SMSPlan(models.Model):
    '''Plano de SMS Adicional'''

    sms_pack_size = models.PositiveIntegerField(
        verbose_name='Pacote de SMS',
        null=True,
        blank=True
    )

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
        max_digits=8
    )

    unlimited = models.BooleanField(
        verbose_name='Ilimitados',
        default=False
    )

    def __str__(self):
        if self.unlimited:
            return 'SMS ILIMITADOS'
        return '{} SMS'.format(self.sms_pack_size)

    class Meta:
        verbose_name = 'Plano de SMS Adicional'
        verbose_name_plural = 'Planos de SMS Adicionais'
        ordering = ['sms_pack_size']


class DataPlan(models.Model):
    '''Plano de Dados Adicional'''

    data_mb = models.IntegerField(
        verbose_name='Pacote de dados (MB)',
    )

    data_unit = models.CharField(
        verbose_name='Pacote de dados (unidade)',
        choices=(('MB', 'Megabyte'), ('GB', 'Gigabyte')),
        max_length=2
    )

    value = models.DecimalField(
        verbose_name='Valor',
        decimal_places=2,
        max_digits=8
    )

    def __str__(self):
        if self.data_unit == 'MB':
            return '{}MB'.format(self.data_mb)
        else:
            return '{}GB'.format(self.data_mb // 1024)

    class Meta:
        verbose_name = 'Plano de Dados Adicional'
        ordering = ['data_mb']
