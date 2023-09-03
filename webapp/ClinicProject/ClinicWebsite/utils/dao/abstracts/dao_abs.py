from abc import ABC, abstractmethod
from django.db import connection
from dataclasses import make_dataclass, dataclass
from django.db import models


# class DAOAbstract(ABC):
#
#     @staticmethod
#     @abstractmethod
#     def from_orm_to_entity(obj: models.Model) -> dataclass:
#         pass


class DAO:
    """
    It is universal DAO class which dynamic make dataclass by make_dataclass() and
    return this.
    It is necessary to enter the name of the attributes.
    If it is necessary you can enter name of fields which may not be in model,
    for example, it can be field of photo.
    """

    def __init__(self, names_of_attrs, exceptions=None):
        self.names_of_attrs = names_of_attrs
        self.exceptions = exceptions

    @staticmethod
    def verify_attrs(model, names_of_attrs: list, exceptions: str):
        try:
            if model.__getattribute__(exceptions):
                names_of_attrs.append(exceptions)
        except AttributeError as error:
            print(error)
        except Exception as error:
            print(error)

        return names_of_attrs

    def fill_universal_data_class(self, model, *args, **kwargs) -> dataclass:

        lst_of_names_of_fields = self.verify_attrs(model, self.names_of_attrs, self.exceptions)
        lst_of_types_of_fields = []
        lst_of_attrs = []
        for i in range(len(self.names_of_attrs)):

            try:
                lst_of_types_of_fields.append(type(model.__getattribute__(self.names_of_attrs[i])))

                lst_of_attrs.append(model.__getattribute__(self.names_of_attrs[i]))
            except AttributeError as err:
                print(err)
            except Exception as err:
                print(err)

        lst_of_fields = list(zip(lst_of_names_of_fields, lst_of_types_of_fields))

        some_data_class = make_dataclass('universalDataClass', lst_of_fields)

        return some_data_class(*lst_of_attrs)
