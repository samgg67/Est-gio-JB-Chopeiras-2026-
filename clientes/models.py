from django.db import models


class Clientes(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=150)

    tempo_de_fidelidade = models.IntegerField( default=0)

    servicos_realizados = models.IntegerField( default=0)

    deletado_em = models.DateTimeField( null=True, blank=True)

    @property
    def ativo(self):
        return self.deletado_em is None

    def __str__(self):
        return self.nome