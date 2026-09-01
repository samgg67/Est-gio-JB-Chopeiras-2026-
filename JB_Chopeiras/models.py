from django.db import models


class Relatorio(models.Model):
    mes = models.PositiveIntegerField()
    ano = models.PositiveIntegerField()
    total = models.PositiveIntegerField(default=0)
    pendentes = models.PositiveIntegerField(default=0)
    andamento = models.PositiveIntegerField(default=0)
    finalizados = models.PositiveIntegerField(default=0)
    total_clientes = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'relatorios'

    def __str__(self):
        return f'Relatório {self.mes}/{self.ano}'
