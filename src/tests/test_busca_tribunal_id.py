import unittest
from unittest.mock import patch
from src.app.db_services import buscar_tribunal_por_id

@patch('src.app.db_services.sqlite3.connect')
def test_buscar_tribunal_por_id_existente(self, mock_connect):
    tribunal_id = '02'

    # Configuração do mock para retornar um resultado válido
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = ('02', 'AL', 'https://www2.tjal.jus.br')

    # Execução da função a ser testada
    tribunal = buscar_tribunal_por_id(tribunal_id)

    # Verificação do resultado
    self.assertEqual(tribunal.tribunal_id, '02')
    self.assertEqual(tribunal.uf, 'AL')
    self.assertEqual(tribunal.base_url, 'https://www2.tjal.jus.br')

    # Verificação das chamadas de função
    mock_connect.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM tribunais WHERE tribunal_id = ?", ('02',))
    mock_cursor.fetchone.assert_called_once()
    mock_connect.return_value.close.assert_called_once()


@patch('src.app.db_services.sqlite3.connect')
def test_buscar_tribunal_por_id_inexistente(self, mock_connect):
    tribunal_id = '99'

    # Configuração do mock para retornar None, simulando um resultado inexistente
    mock_cursor = mock_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None

    # Execução da função a ser testada
    tribunal = buscar_tribunal_por_id(tribunal_id)

    # Verificação do resultado
    self.assertIsNone(tribunal)

    # Verificação das chamadas de função
    mock_connect.assert_called_once()
    mock_cursor.execute.assert_called_once_with("SELECT * FROM tribunais WHERE tribunal_id = ?", ('99',))
    mock_cursor.fetchone.assert_called_once()
    mock_connect.return_value.close.assert_called_once()
