from app.storages.database_filter import format_to_database_filter


def test_deve_formar_dado_aninhado():
    query = {'obj1': {'obj2': 'dado2'}}
    resultado = format_to_database_filter(query)
    assert resultado == {'obj1.obj2': 'dado2'}


def test_mais_de_um_dado_aninhado_deve_funcionar():
    query = {'obj1': {'obj2': 'dado2', 'obj3': 'dado3'}}
    resultado = format_to_database_filter(query)
    assert resultado == {'obj1.obj2': 'dado2', 'obj1.obj3': 'dado3'}


def test_dado_vazio_deve_retornar_vazio():
    query = {}
    resultado = format_to_database_filter(query)
    assert resultado == {}


def test_dados_incorretos_devem_retornar_vazio():
    query = {'obj1': {'obj2': {}}}
    resultado = format_to_database_filter(query)
    assert resultado == {}
