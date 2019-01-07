# -*- coding: utf-8 -*-
from django.db import models


class QuerySet(models.QuerySet):

    def class_name(self):
        return self.__class__.__name__


class QuerySetManager(models.Manager):

    def get_queryset(self):
        return QuerySet(self.model, using=self._db)

    def class_name(self):
        return self.get_queryset().class_name()
