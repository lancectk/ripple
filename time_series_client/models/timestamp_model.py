from django.db import models
from django.utils import timezone
from datetime import datetime
from django_unixdatetimefield import UnixDateTimeField

from time_series_client.models.managers.core_manager import CoreManager

class TimestampModel(models.Model):
    """
    TimestampModel objects have a created_at and a committed_at field.
    Typically used for maintaining timeseries

    """
    objects = CoreManager()

    # https://pypi.python.org/pypi/django-unixdatetimefield/
    #   django unix time field provides accessors
    created_at     = UnixDateTimeField(default=timezone.now, null=False)
    committed_at   = UnixDateTimeField(null=True)

    datetime_format = '%Y-%m-%d %H:%M %Z'

    class Meta:
        abstract = True

    @classmethod
    def format_datetime(cls, dt):
        return dt.strftime(cls.datetime_format)

    @property
    def created_at_datetime(self):
        """
        Convenience method to get object's created_at timestamp in python datetime format
        :return:
        """
        return TimestampModel.format_datetime(datetime.fromtimestamp(self.created_at))

    @property
    def committed_at_datetime(self):
        """
        Convenience method to get object's committed_at timestamp in python datetime format
        :return:
        """
        return TimestampModel.format_datetime(datetime.fromtimestamp(self.committed_at))

    def __str__(self):
        return f'Object of class {type(self)} | Created at {self.created_at} | Committed at {self.committed_at}'