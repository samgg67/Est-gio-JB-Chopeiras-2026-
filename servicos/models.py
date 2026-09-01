from django.core.validators import RegexValidator
from django.conf import settings
from django.db import models
from django.db.models import Max
from django.utils import timezone


class Servico(models.Model):
    STATUS_CHOICES = [('p', 'Pendente'), ('a', 'Em andamento'), ('f', 'Finalizado')]

    protocolo = models.PositiveIntegerField(unique=True, editable=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='solicitacoes',
        null=True,
        blank=True,
    )
    nome = models.CharField(max_length=50, validators=[
        RegexValidator(r'^[A-Za-zÀ-ÿ\s]+$', 'O nome deve conter apenas letras e espaços.')
    ])
    email = models.EmailField(max_length=50)
    telefone = models.CharField(max_length=20, blank=True, default='', validators=[
        RegexValidator(r'^\d+$', 'O telefone deve conter apenas números.')
    ])
    endereco = models.CharField(max_length=50)
    problema = models.CharField(max_length=20)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    notas = models.CharField(max_length=250, blank=True)
    quantidade = models.PositiveIntegerField(default=1)
    previsao_entrega = models.DateField(null=True, blank=True)
    criado_em = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        db_table = 'servicos'
        ordering = ['-protocolo']

    def save(self, *args, **kwargs):
        if not self.pk:
            maior = Servico.objects.aggregate(maior=Max('protocolo'))['maior']
            self.protocolo = (maior or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Protocolo {self.protocolo} - {self.nome}'
