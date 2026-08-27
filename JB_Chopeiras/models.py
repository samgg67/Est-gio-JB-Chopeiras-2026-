from django.db import models


class Solicitacao(models.Model):

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('andamento', 'Em andamento'),
        ('finalizado', 'Finalizado'),
    ]

    nome = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    problema = models.CharField( max_length=200 )

    endereco = models.CharField( max_length=255 )

    explicacao = models.TextField()

    data_criacao = models.DateTimeField( auto_now_add=True )

    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='pendente' )

    def __str__(self):
        return f'{self.nome} - {self.problema}'

class Relatorio(models.Model):

    mes = models.PositiveIntegerField()

    ano = models.PositiveIntegerField()

    total = models.PositiveIntegerField(default=0)

    pendentes = models.PositiveIntegerField(default=0)

    andamento = models.PositiveIntegerField(default=0)

    finalizados = models.PositiveIntegerField(default=0)

    total_clientes = models.PositiveIntegerField(default=0)

    criado_em = models.DateTimeField( auto_now_add=True )

    def __str__(self):
        return f'Relatório {self.mes}/{self.ano}'