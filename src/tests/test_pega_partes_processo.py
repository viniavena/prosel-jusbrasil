import unittest
from bs4 import BeautifulSoup
from app.scrap import pega_partes_do_processo, ParteDoProcesso

class TestPegaPartesDoProcesso(unittest.TestCase):

    def setUp(self):
        self.html_partes = """
            <table id="tableTodasPartes">
                <tr class="fundoClaro">
                    <span class="mensagemExibindo tipoDeParticipacao">Tipo de Parte 1</span>
                    <td class="nomeParteEAdvogado">Nome Parte 1</td>
                    <span>Advogado: </span>Advogado 1
                    <span>Advogada: </span>Advogado 2
                </tr>
                <tr class="fundoClaro">
                    <span class="mensagemExibindo tipoDeParticipacao">Tipo de Parte 2</span>
                    <td class="nomeParteEAdvogado">Nome Parte 2</td>
                    <span>Advogade: </span>Advogado 3
                </tr>
            </table>
        """

    def test_pega_partes_do_processo(self):
        soup = BeautifulSoup(self.html_partes, 'html.parser')

        partes = pega_partes_do_processo(soup)

        self.assertIsInstance(partes, list)
        self.assertEqual(len(partes), 2)

        parte_1 = partes[0]
        self.assertIsInstance(parte_1, ParteDoProcesso)
        self.assertEqual(parte_1.tipo_parte, "Tipo de Parte 1")
        self.assertEqual(parte_1.nome_parte, "Nome Parte 1")
        self.assertListEqual(parte_1.advogados, ["Advogado 1", "Advogado 2"])

        parte_2 = partes[1]
        self.assertIsInstance(parte_2, ParteDoProcesso)
        self.assertEqual(parte_2.tipo_parte, "Tipo de Parte 2")
        self.assertEqual(parte_2.nome_parte, "Nome Parte 2")
        self.assertListEqual(parte_2.advogados, ["Advogado 3"])

    def test_pega_partes_do_processo_sem_partes(self):
        soup = BeautifulSoup("<table></table>", 'html.parser')

        partes = pega_partes_do_processo(soup)

        self.assertEqual(len(partes), 0)

if __name__ == '__main__':
    unittest.main()
