from dao_abs import DAO


class Model:

    def __init__(self, pk, name, field):
        self.pk = pk
        self.name = name
        self.field = field


model = Model(1, 'andrey', '+79017877058')

res = DAO.fill_universal_data_class(pk=model.pk, name=model.name, field=model.field)

print(res)
