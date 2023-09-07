from dataclasses import dataclass

from typing import Iterable

from ClinicWebsite.utils.dao.dao import DAOForModels
from django.db import models

from ..abstracts.get_abc import GetQueryAbstract


class GetQuery(GetQueryAbstract):

    def get_query(self, some_model: models.Model, *args, exceptions: str = None, **kwargs,):
        dao = DAOForModels(args, exceptions)
        return list(map(dao.fill_universal_data_class, some_model.objects.get(**kwargs)))
