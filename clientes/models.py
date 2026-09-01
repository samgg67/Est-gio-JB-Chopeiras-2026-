from django.conf import settings
from django.db import models


class Clientes(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_cliente',
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=150)

    tempo_de_fidelidade = models.IntegerField(default=0)
    servicos_realizados = models.IntegerField(default=0)
    deletado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'clientes'

    @property
    def ativo(self):
        return self.deletado_em is None

    def __str__(self):
        return self.nome


class PerguntaFrequente(models.Model):
    pergunta = models.CharField(max_length=200)
    resposta = models.TextField()
    ordem = models.PositiveIntegerField(default=0)
    ativa = models.BooleanField(default=True)

    class Meta:
        db_table = 'perguntas_frequentes'
        ordering = ['ordem', 'id']
        verbose_name = 'pergunta frequente'
        verbose_name_plural = 'perguntas frequentes'

    def __str__(self):
        return self.pergunta


class LocalizacaoEmpresa(models.Model):
    nome = models.CharField(max_length=100, default='JB Chopeiras')
    endereco = models.CharField(max_length=180)
    cidade = models.CharField(max_length=80, default='Londrina')
    estado = models.CharField(max_length=2, default='PR')
    cep = models.CharField(max_length=9, blank=True)
    telefone = models.CharField(max_length=20)
    horario_atendimento = models.CharField(max_length=150)
    url_mapa = models.URLField(max_length=500)
    numero_whatsapp = models.CharField(
        max_length=20,
        help_text='Somente números, incluindo código do país e DDD.',
    )
    ativa = models.BooleanField(default=True)

    class Meta:
        db_table = 'localizacoes'
        verbose_name = 'localização da empresa'
        verbose_name_plural = 'localizações da empresa'

    def __str__(self):
        return f'{self.nome} - {self.cidade}/{self.estado}'
