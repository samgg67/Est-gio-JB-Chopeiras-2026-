from django.db import models

class Servico(models.Model):
    STATUS_CHOICES = [
        ('p', 'Pendente'),
        ('a', 'Andamento'),
        ('f', 'Finalizado'),
    ]

    protocolo = models.IntegerField (blank= False)
    nome = models.CharField(max_length=50, blank=False)
    email = models.EmailField(max_length=50)
    telefone = models.CharField(max_length= 14)
    endereco = models.CharField(max_length=20, blank=False)
    problema = models.CharField(max_length=20, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    notas = models.CharField (max_length=250)

    def __str__(self):
        return self.protocolo
    