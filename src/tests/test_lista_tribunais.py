import unittest
from unittest.mock import patch
from src.app.db_services import listar_tribunais, Tribunal

class TestListarTribunais(unittest.TestCase):
    def setUp(self):
        # Configuração inicial dos testes
        self.resultados = [
            ('02', 'AL', 'https://www2.tjal.jus.br'),
            ('06', 'CE', 'https://esaj.tjce.jus.br')
        ]

    @patch('src.app.db_services.sqlite3.connect')
    def test_listar_tribunais(self, mock_connect):
        # Configuração do mock para o objeto de conexão
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = self.resultados

        # Execução da função a ser testada
        tribunais = listar_tribunais()

        # Verificação dos resultados
        self.assertEqual(len(tribunais), 2)
        self.assertIsInstance(tribunais[0], Tribunal)
        self.assertEqual(tribunais[0].tribunal_id, '02')
        self.assertEqual(tribunais[0].uf, 'AL')
        self.assertEqual(tribunais[0].base_url, 'https://www2.tjal.jus.br')

        self.assertIsInstance(tribunais[1], Tribunal)
        self.assertEqual(tribunais[1].tribunal_id, '06')
        self.assertEqual(tribunais[1].uf, 'CE')
        self.assertEqual(tribunais[1].base_url, 'https://esaj.tjce.jus.br')

        # Verificação das chamadas de função
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM tribunais")
        mock_cursor.fetchall.assert_called_once()
        mock_connect.return_value.close.assert_called_once()

    @patch('src.app.db_services.sqlite3.connect')
    def test_listar_tribunais_vazio(self, mock_connect):
        # Configuração do mock para retornar uma conexão e um cursor vazios
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []

        # Execução da função a ser testada
        tribunais = listar_tribunais()

        # Verificação do resultado
        self.assertEqual(len(tribunais), 0)

        # Verificação das chamadas de função
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM tribunais")
        mock_cursor.fetchall.assert_called_once()
        mock_connect.return_value.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()