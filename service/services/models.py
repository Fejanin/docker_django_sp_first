from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_delete
from clients.models import Client
from services.receivers import delete_cache_total_sum
from services.tasks import set_price, set_comment


class Service(models.Model):
    name = models.CharField(max_length=50)
    full_price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if self.__full_price != self.full_price:
            for subscription in self.suscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return obj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def __str__(self):
        return f'Service: {self.name}'


class Plan(models.Model):
    PLAN_TYPES = (
        ('full', 'Full'),
        ('student', 'Student'),
        ('discount', 'Discount'),
    )

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=10)
    discount_percent = models.PositiveIntegerField(default=0,
                                                   validators=[
                                                       MaxValueValidator(100)
                                                   ])

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if self.__discount_percent != self.discount_percent:
            for subscription in self.suscriptions.all():
                set_price.delay(subscription.id)
                set_comment.delay(subscription.id)
        return obj

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def __str__(self):
        return f'{self.plan_type}'


class Subscription(models.Model):
    client = models.ForeignKey(Client, related_name='suscriptions', on_delete=models.PROTECT)
    service = models.ForeignKey(Service, related_name='suscriptions', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, related_name='suscriptions', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=50, default='')

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        obj = super().save(*args, **kwargs)
        if creating:
            set_price.delay(self.id)
        return obj

    def __str__(self):
        return f'{self.client} is subscribed to the service {self.service} according to the tariff plan {self.plan}'


post_delete.connect(delete_cache_total_sum, sender=Subscription)
