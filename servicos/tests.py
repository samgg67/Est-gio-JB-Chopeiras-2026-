from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Servico


class ServicoModelTests(TestCase):
    def test_protocolo_e_incrementado_sem_reutilizar_numero_excluido(self):
        primeiro = Servico.objects.create(
            nome='Ana', email='ana@example.com', telefone='43999999999',
            endereco='Rua A', problema='Manutencao',
        )
        segundo = Servico.objects.create(
            nome='Bruno', email='bruno@example.com', telefone='43888888888',
            endereco='Rua B', problema='Instalacao',
        )
        primeiro.delete()
        terceiro = Servico.objects.create(
            nome='Carla', email='carla@example.com', telefone='43777777777',
            endereco='Rua C', problema='Limpeza',
        )

        self.assertEqual(segundo.protocolo, 2)
        self.assertEqual(terceiro.protocolo, 3)


class ServicoViewTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            username='admin', password='senha-forte', is_staff=True,
        )

    def test_lista_exige_autenticacao(self):
        resposta = self.client.get(reverse('servicos:lista'))
        self.assertRedirects(
            resposta,
            f"{reverse('tela_entrada')}?next={reverse('servicos:lista')}",
        )

    def test_staff_acessa_dashboard_e_lista(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(reverse('servicos:dashboard')).status_code, 200)
        self.assertEqual(self.client.get(reverse('servicos:lista')).status_code, 200)

    def test_lista_pesquisa_e_filtra_solicitacoes(self):
        Servico.objects.create(
            nome='Ana', email='ana@example.com', telefone='43999999999',
            endereco='Rua A', problema='Vazamento', status='p',
        )
        Servico.objects.create(
            nome='Bruno', email='bruno@example.com', telefone='43888888888',
            endereco='Rua B', problema='Limpeza', status='f',
        )
        self.client.force_login(self.staff)

        pesquisa = self.client.get(reverse('servicos:lista'), {'q': 'Ana'})
        self.assertContains(pesquisa, 'Vazamento')
        self.assertNotContains(pesquisa, 'Limpeza')

        finalizadas = self.client.get(reverse('servicos:lista'), {'status': 'f'})
        self.assertContains(finalizadas, 'Limpeza')
        self.assertNotContains(finalizadas, 'Vazamento')

    def test_formulario_publico_cria_servico(self):
        self.client.force_login(self.staff)
        resposta = self.client.post(reverse('servicos:solicitar'), {
            'nome': 'Samuel',
            'email': 'samuel@example.com',
            'telefone': '43999999999',
            'problema': 'Manutencao',
            'endereco': 'Rua Principal',
            'explicacao': 'A chopeira nao esta gelando.',
        })
        self.assertRedirects(resposta, reverse('servicos:sucesso'))
        self.assertEqual(Servico.objects.count(), 1)
