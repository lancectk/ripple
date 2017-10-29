from django.db import models

from django.core.exceptions import ObjectDoesNotExist

class CoreManager(models.Manager):
    """
    Set of basic functionality that we wish Django had. These are generic and non-application specific.
    Should be refactored to a lib for use in all Cresta apps
    """


    def get_or_none(self, **kwargs):
        """
        Attempts to get an object in the Model, returns None if object does not exist
        :param kwargs: filter params
        :return:
        """
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


    def get_latest_or_none(self, latest_field, **kwargs):
        """
        Attempts to get latest object in the Model, returns None if object does not exist

        :param latest_field: field to sort by
        :param kwargs: filter params
        :return:
        """
        try:
            return self.filter(**kwargs).latest(latest_field)
        except ObjectDoesNotExist:
            return None