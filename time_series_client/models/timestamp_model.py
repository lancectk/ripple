from django.db import models
from datetime import datetime

from django_unixdatetimefield import UnixDateTimeField

class TimestampModel(models.Model):
    """
    TimestampModel objects have a created_at and a committed_at field.
    Typically used for maintaining timeseries

    """

    # https://pypi.python.org/pypi/django-unixdatetimefield/
    #   django unix time field provides accessors
    created_at     = UnixDateTimeField()
    committed_at   = UnixDateTimeField()

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
        return ('Object of class {} | Created at {} | Committed at {}'
                .format(type(self), self.created_at_datetime(), self.committed_at_datetime()))