from django.db import models

class Clientes(models.Model):
    nome = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=50, blank=False)
    tempo_de_fidelidade = models.IntegerField()
    servicos_realizados = models.IntegerField()


    def __str__(self):
        return self.protocolo