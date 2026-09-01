from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Clientes, LocalizacaoEmpresa, PerguntaFrequente
from servicos.models import Servico


class DuvidasTests(TestCase):
    def test_pagina_e_publica(self):
        resposta = self.client.get(reverse('duvidas'))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'clientes/duvidas.html')

    def test_exibe_somente_perguntas_ativas(self):
        PerguntaFrequente.objects.create(
            pergunta='Pergunta visível?', resposta='Sim.', ordem=1, ativa=True,
        )
        PerguntaFrequente.objects.create(
            pergunta='Pergunta oculta?', resposta='Não.', ordem=2, ativa=False,
        )
        resposta = self.client.get(reverse('duvidas'))
        self.assertContains(resposta, 'Pergunta visível?')
        self.assertNotContains(resposta, 'Pergunta oculta?')

    def test_pagina_de_localizacao(self):
        LocalizacaoEmpresa.objects.create(
            nome='JB Chopeiras', endereco='Av. São João, 2935',
            telefone='(43) 98402-2769',
            horario_atendimento='Segunda a sexta, das 8h às 18h',
            url_mapa='https://maps.google.com/',
            numero_whatsapp='5543984022769',
        )
        resposta = self.client.get(reverse('localizacao'))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'clientes/localizacao.html')
        self.assertContains(resposta, 'Av. São João, 2935')


class HistoricoTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='cliente@example.com',
            email='cliente@example.com',
            password='senha-forte',
        )
        Servico.objects.create(
            nome='Cliente', email='cliente@example.com', telefone='43999999999',
            endereco='Rua A', problema='Vazamento', quantidade=2,
        )
        Servico.objects.create(
            nome='Outro', email='outro@example.com', telefone='43888888888',
            endereco='Rua B', problema='Limpeza',
        )

    def test_historico_exige_login(self):
        resposta = self.client.get(reverse('historico'))
        self.assertRedirects(
            resposta,
            f"{reverse('tela_entrada')}?next={reverse('historico')}",
        )

    def test_historico_mostra_apenas_servicos_do_usuario(self):
        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse('historico'))
        self.assertContains(resposta, 'Vazamento')
        self.assertNotContains(resposta, 'Limpeza')

    def test_historico_filtra_solicitacoes_por_status(self):
        solicitacao = Servico.objects.get(email='cliente@example.com')
        solicitacao.status = 'f'
        solicitacao.save(update_fields=['status'])
        self.client.force_login(self.usuario)

        finalizadas = self.client.get(reverse('historico'), {'status': 'f'})
        self.assertContains(finalizadas, 'Vazamento')
        self.assertEqual(finalizadas.context['resumo']['finalizados'], 1)

        pendentes = self.client.get(reverse('historico'), {'status': 'p'})
        self.assertNotContains(pendentes, 'Vazamento')
        self.assertContains(pendentes, 'Nenhuma solicitação com esse status')


class ContaClienteTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='conta@example.com',
            email='conta@example.com',
            password='senha-antiga-123',
        )
        self.cliente = Clientes.objects.create(
            usuario=self.usuario,
            nome='Cliente Teste',
            email='conta@example.com',
            telefone='43999999999',
            endereco='Rua Antiga',
        )
        self.client.force_login(self.usuario)

    def test_atualiza_perfil(self):
        resposta = self.client.post(reverse('perfil_cliente'), {
            'nome': 'Nome Atualizado',
            'telefone': '(43) 98888-7777',
            'endereco': 'Rua Nova, 100',
        })
        self.assertEqual(resposta.status_code, 200)
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.nome, 'Nome Atualizado')
        self.assertContains(resposta, 'Perfil atualizado com sucesso.')

    def test_troca_senha_e_mantem_sessao(self):
        resposta = self.client.post(reverse('trocar_senha'), {
            'old_password': 'senha-antiga-123',
            'new_password1': 'Nova-senha-segura-456',
            'new_password2': 'Nova-senha-segura-456',
        })
        self.assertEqual(resposta.status_code, 200)
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password('Nova-senha-segura-456'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_solicitacao_enviada_aparece_no_historico(self):
        resposta = self.client.post(reverse('servicos:solicitar'), {
            'nome': 'Cliente Teste',
            'telefone': '43999999999',
            'problema': 'Vazamento',
            'endereco': 'Rua Antiga',
            'explicacao': 'A chopeira não está gelando.',
        })
        self.assertRedirects(resposta, reverse('servicos:sucesso'))

        solicitacao = Servico.objects.get(problema='Vazamento')
        self.assertEqual(solicitacao.usuario, self.usuario)
        self.assertEqual(solicitacao.email, self.usuario.email)

        historico = self.client.get(reverse('historico'))
        self.assertContains(historico, 'Vazamento')
