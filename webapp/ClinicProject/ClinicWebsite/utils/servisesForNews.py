from datetime import datetime
from ..models import *
from dataclasses import dataclass
from typing import Generator
from typing import Iterable


@dataclass
class NewEntity:
    pk: int
    title: str
    text: str
    slug: str
    photo: str
    time_create: datetime
    time_update: datetime
    is_published: bool
    get_absolute_url: str


class doSomeThingWithNews:

    @staticmethod
    def from_orm_to_entity(new: News) -> NewEntity:
        # for new in News.objects.all():
        return NewEntity(
            pk=new.pk,
            title=new.title,
            text=new.text,
            slug=new.slug,
            photo=new.photo,
            time_create=new.time_create,
            time_update=new.time_update,
            is_published=new.is_published,
            get_absolute_url=new.get_absolute_url()
        )

    def fetch_all_news(self) -> Iterable[NewEntity]:
        return list(map(self.from_orm_to_entity, News.objects.all()))

    def fetch_one_new(self, slug: str) -> NewEntity:
        return self.from_orm_to_entity(News.objects.get(slug=slug))
