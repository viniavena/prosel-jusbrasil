import unittest
from bs4 import BeautifulSoup
from app.scrap import pega_infos_processo, ParteDoProcesso, MovimentacaoProcesso, DadosProcesso

class TestPegaInfosProcesso(unittest.TestCase):

    def setUp(self):
        self.html_processo = """
            <span id="numeroProcesso">123456</span>
            <span id="juizProcesso">Juiz Fulano</span>
            <span id="assuntoProcesso">Assunto do Processo</span>
            <span id="classeProcesso">Classe do Processo</span>
            <div id="dataHoraDistribuicaoProcesso">01/01/2023</div>
            <div id="valorAcaoProcesso">R$ 1000,00</div>
            <div id="areaProcesso">Área do Processo</div>
            <table id="tableTodasPartes">
                <tr class="fundoClaro">
                    <span class="mensagemExibindo tipoDeParticipacao">Tipo de Parte 1</span>
                    <td class="nomeParteEAdvogado">Nome Parte 1</td>
                    <span>Advogade: </span>Advogado 1
                </tr>
            </table>

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
        self.html_processo_sem_movimentacoes = """
            <span id="numeroProcesso">123456</span>
            <span id="juizProcesso">Juiz Fulano</span>
            <span id="assuntoProcesso">Assunto do Processo</span>
            <span id="classeProcesso">Classe do Processo</span>
            <div id="dataHoraDistribuicaoProcesso">01/01/2023</div>
            <div id="valorAcaoProcesso">R$ 1000,00</div>
            <div id="areaProcesso">Área do Processo</div>
            <table id="tableTodasPartes">
                <tr class="fundoClaro">
                    <span class="mensagemExibindo tipoDeParticipacao">Tipo de Parte 1</span>
                    <td class="nomeParteEAdvogado">Nome Parte 1</td>
                    <span>Advogade: </span>Advogado 1
                </tr>
            </table>
        """

        self.html_processo_sem_partes = """
            <span id="numeroProcesso">123456</span>
            <span id="juizProcesso">Juiz Fulano</span>
            <span id="assuntoProcesso">Assunto do Processo</span>
            <span id="classeProcesso">Classe do Processo</span>
            <div id="dataHoraDistribuicaoProcesso">01/01/2023</div>
            <div id="valorAcaoProcesso">R$ 1000,00</div>
            <div id="areaProcesso">Área do Processo</div>
            <table id="tabelaTodasMovimentacoes">
                <tbody>
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
            </table>
        """

        self.html_processo_sem_partes_e_movimentacoes = """
            <span id="numeroProcesso">123456</span>
            <span id="juizProcesso">Juiz Fulano</span>
            <span id="assuntoProcesso">Assunto do Processo</span>
            <span id="classeProcesso">Classe do Processo</span>
            <div id="dataHoraDistribuicaoProcesso">01/01/2023</div>
            <div id="valorAcaoProcesso">R$ 1000,00</div>
            <div id="areaProcesso">Área do Processo</div>
        """


    def test_pega_infos_processo_completo(self):
        soup = BeautifulSoup(self.html_processo, 'html.parser')
        numero_processo = "123456"
        grau_instancia = 1

        dados_processo = pega_infos_processo(soup, numero_processo, grau_instancia)

        self.assertIsInstance(dados_processo, DadosProcesso)
        self.assertEqual(dados_processo.numero_processo, "123456")
        self.assertEqual(dados_processo.juiz, "Juiz Fulano")
        self.assertEqual(dados_processo.assunto, "Assunto do Processo")
        self.assertEqual(dados_processo.classe, "Classe do Processo")
        self.assertEqual(dados_processo.data_distribuicao, "01/01/2023")
        self.assertEqual(dados_processo.valor_acao, "R$1000,00")
        self.assertEqual(dados_processo.area, "Área do Processo")

        partes = dados_processo.partes
        self.assertEqual(len(partes), 1)
        parte = partes[0]
        self.assertIsInstance(parte, ParteDoProcesso)
        self.assertEqual(parte.tipo_parte, "Tipo de Parte 1")
        self.assertEqual(parte.nome_parte, "Nome Parte 1")
        self.assertEqual(parte.advogados, ["Advogado 1"])

        movimentacoes = dados_processo.movimentacoes
        self.assertEqual(len(movimentacoes), 2)
        movimentacao = movimentacoes[0]
        self.assertIsInstance(movimentacao, MovimentacaoProcesso)
        self.assertEqual(movimentacao.data_movimentacao, "01/01/2023")
        self.assertEqual(movimentacao.tramite, "Tramite 1")
        self.assertEqual(movimentacao.descricao, "Descrição 1")

    def test_pega_infos_processo_sem_partes(self):
        soup = BeautifulSoup(self.html_processo_sem_partes, 'html.parser')
        numero_processo = "123456"
        grau_instancia = 1

        dados_processo = pega_infos_processo(soup, numero_processo, grau_instancia)

        self.assertIsInstance(dados_processo, DadosProcesso)
        partes = dados_processo.partes
        self.assertEqual(len(partes), 0)

    def test_pega_infos_processo_sem_movimentacoes(self):
        soup = BeautifulSoup(self.html_processo_sem_movimentacoes, 'html.parser')
        numero_processo = "123456"
        grau_instancia = 1

        dados_processo = pega_infos_processo(soup, numero_processo, grau_instancia)

        self.assertIsInstance(dados_processo, DadosProcesso)
        movimentacoes = dados_processo.movimentacoes
        self.assertEqual(len(movimentacoes), 0)

    def test_pega_infos_processo_sem_partes_e_movimentacoes(self):
        soup = BeautifulSoup(self.html_processo_sem_partes_e_movimentacoes, 'html.parser')
        numero_processo = "123456"
        grau_instancia = 1

        dados_processo = pega_infos_processo(soup, numero_processo, grau_instancia)

        self.assertIsInstance(dados_processo, DadosProcesso)
        partes = dados_processo.partes
        self.assertEqual(len(partes), 0)
        movimentacoes = dados_processo.movimentacoes
        self.assertEqual(len(movimentacoes), 0)

if __name__ == '__main__':
    unittest.main()
