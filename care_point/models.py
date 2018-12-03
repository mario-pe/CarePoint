from account.models import User
from datetime import datetime
from django.db import models


class Point_of_care(models.Model):
    city = models.CharField(max_length=30)

    def __str__(self):
        return self.city


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    point_of_care = models.ForeignKey(Point_of_care, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.user, self.point_of_care)


class Caregiver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    point_of_care = models.ForeignKey(Point_of_care, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.user, self.point_of_care)


class Contract(models.Model):
    CONTRACT_TYPE = (
        ('umowa', 'umowa'),
        ('zlecenie', 'zlecenie')
    )
    genre = models.CharField(max_length=20,
                             choices=CONTRACT_TYPE,
                             default='umowa')
    date_from = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=True, null=True)
    date_to = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=True, null=True)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '{}, {}  {}, {}'.format(self.genre, self.date_from, self.date_to, self.caregiver)


class Ward(models.Model):
    name = models.CharField(max_length=30)
    sname = models.CharField(max_length=30)
    pesel = models.CharField(max_length=15)

    def __str__(self):
        return '{}, {}'.format(self.name, self.sname)


class Address(models.Model):
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    number = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return '{}, ul.  {}, {}, kod pocztowy {}'.format(self.city, self.street, self.number, self.zip_code)


class Illness(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}.'.format(self.name, self.description)


class Activity(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}'.format(self.name, self.description)


class Decision(models.Model):
    percent_payment = models.CharField(max_length=5)
    hours = models.CharField(max_length=4)
    charge = models.CharField(max_length=30)
    ward = models.ForeignKey(Ward, blank=True, null=True, on_delete=models.CASCADE)
    illness = models.ManyToManyField(Illness, blank=True)
    activity = models.ManyToManyField(Activity, blank=True)

    def __str__(self):
        return 'Doplata w {}%, godziny {}, stawka {}, podopieczny {}'.format(self.percent_payment, self.hours, self.charge, self.ward)


class Worksheet(models.Model):
    CONTRACT_TYPE = (
        ('umowa', 'umowa'),
        ('zlecenie', 'zlecenie')
    )
    genre = models.CharField(max_length=15,
                             choices=CONTRACT_TYPE,
                             default='umowa')
    date = models.DateField(default=datetime.now().strftime("%Y-%m-%d"), blank=True, null=True)
    hour_from = models.TimeField(default='8:00')
    hour_to = models.TimeField(default='10:00')
    description = models.CharField(max_length=200)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE)
    decision = models.ForeignKey(Decision, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'opiekun {}, podopieczny {}, date {}, {} - {} '.format(self.caregiver, self.ward, self.date, self.hour_from, self.hour_to)


class WardIllness(models.Model):
    ward = models.ForeignKey(Ward, blank=True, null=True, on_delete=models.CASCADE)
    illness = models.ForeignKey(Illness, blank=True, null=True, on_delete=models.CASCADE)
    decision = models.ForeignKey(Decision, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'podopieczny {}, schorzenie {}'.format(self.ward, self.illness)


class WardActivity(models.Model):
    ward = models.ForeignKey(Ward, blank=True, null=True, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.CASCADE)
    decision = models.ForeignKey(Decision, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return 'podopieczny {}, aktywnosc {}'.format(self.ward, self.activity)



