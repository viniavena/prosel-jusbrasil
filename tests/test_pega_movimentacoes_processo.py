import unittest
from bs4 import BeautifulSoup
from app.scrap import pega_movimentacoes_processo, MovimentacaoProcesso

class TestPegaMovimentacoesProcesso(unittest.TestCase):

    def setUp(self):
        self.html_movimentacoes = """
            <tbody id="tabelaTodasMovimentacoes">
                <tr>
                    <td class="dataMovimentacao">01/01/2023</td>
                    <td class="descricaoMovimentacao">
                        <a class="linkMovVincProc" href="#">Tramite 1</a>
                        <span>
                            Descrição 1
                        </span>
                    </td>
                </tr>
                <tr>
                    <td class="dataMovimentacaoProcesso">02/01/2023</td>
                    <td class="descricaoMovimentacaoProcesso">
                        Tramite 2
                        <span>
                            Descrição 2
                        </span>
                    </td>
                </tr>
            </tbody>
        """

    def test_pega_movimentacoes_processo(self):
        soup = BeautifulSoup(self.html_movimentacoes, 'html.parser')
        movimentacoes = pega_movimentacoes_processo(soup)

        self.assertEqual(len(movimentacoes), 2)

        movimentacao1 = movimentacoes[0]
        self.assertIsInstance(movimentacao1, MovimentacaoProcesso)
        self.assertEqual(movimentacao1.data_movimentacao, "01/01/2023")
        self.assertEqual(movimentacao1.tramite, "Tramite 1")
        self.assertEqual(movimentacao1.descricao, "Descrição 1")

        movimentacao2 = movimentacoes[1]
        self.assertIsInstance(movimentacao2, MovimentacaoProcesso)
        self.assertEqual(movimentacao2.data_movimentacao, "02/01/2023")
        self.assertEqual(movimentacao2.tramite, "Tramite 2")
        self.assertEqual(movimentacao2.descricao, "Descrição 2")
        
    def test_pega_movimentacoes_processo_sem_movimentacoes(self):
        soup = BeautifulSoup("", 'html.parser')

        movimentacoes = pega_movimentacoes_processo(soup)

        self.assertEqual(len(movimentacoes), 0)

if __name__ == '__main__':
    unittest.main()
