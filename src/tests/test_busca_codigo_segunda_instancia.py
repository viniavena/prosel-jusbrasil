import unittest
from bs4 import BeautifulSoup

from app.scrap import pega_codigo_segunda_instancia

class TestPegaCodigoSegundaInstancia(unittest.TestCase):
    def test_codigo_presente(self):
        html = '<input id="processoSelecionado" value="P00006BXP0000">'
        soup = BeautifulSoup(html, 'html.parser')
        codigo = pega_codigo_segunda_instancia(soup)
        self.assertEqual(codigo, "P00006BXP0000")

    def test_codigo_ausente(self):
        html = '<div id="mensagemRetorno">Processo não encontrado</div>'
        soup = BeautifulSoup(html, 'html.parser')
        codigo = pega_codigo_segunda_instancia(soup)
        self.assertIsNone(codigo)

    def test_codigo_ausente_sem_mensagem(self):
        html = '<div></div>'
        soup = BeautifulSoup(html, 'html.parser')
        codigo = pega_codigo_segunda_instancia(soup)
        self.assertIsNone(codigo)

if __name__ == '__main__':
    unittest.main()