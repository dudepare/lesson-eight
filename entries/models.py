from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


class Client(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    client = models.ForeignKey('Client', blank=True, null=True)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    def __str__(self):
        return '<{}> {}'.format(self.client, self.name)


# Create your models here.
class Entry(models.Model):
    start = models.DateTimeField(default=timezone.now)
    stop = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey('Project')
    description = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return '[{} - {}] ({}) {}'.format(
            self.start, self.stop, self.project.name, self.description
        )

    def is_finished(self):
        return self.stop is not None

    @property
    def duration(self):
        # assume now for calculating duration
        # if stop is not available
        stop_val = self.stop
        if stop_val is None:
            stop_val = timezone.now()

        elapsed_time = stop_val - self.start
        return (elapsed_time.total_seconds()//datetime.timedelta(minutes=1).total_seconds())
