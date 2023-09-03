from datetime import datetime
from ..models import *
from dataclasses import dataclass
from typing import Generator
from typing import Iterable


@dataclass
class PositionEntity:
    pk: int
    wage: float
    # PlaceOfWork: str
    position: str
    slug: str
    get_absolute_url: str
    get_absolute_url_for_listOfVisits: str


class doSomeThingWithPosition:

    @staticmethod
    def from_orm_to_entity(position: Position) -> PositionEntity:
        return PositionEntity(
            pk=position.pk,
            wage=position.wage,
            # PlaceOfWork=position.PlaceOfWork,
            position=position.position,
            slug=position.slug,
            get_absolute_url=position.get_absolute_url(),
            get_absolute_url_for_listOfVisits=position.get_absolute_url_for_listOfVisits()
        )

    def fetch_all_positions(self) -> Iterable[PositionEntity]:
        return list(map(self.from_orm_to_entity, Position.objects.filter(isDoctor=True)))

    def fetch_one_position(self, slug: str) -> PositionEntity:
        return self.from_orm_to_entity(Position.objects.get(slug=slug))



