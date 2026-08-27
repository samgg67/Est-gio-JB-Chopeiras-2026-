from django.db import models, transaction
from django.core.validators import RegexValidator


class Servico(models.Model):
    STATUS_CHOICES = [
        ('p', 'Pendente'),
        ('a', 'Andamento'),
        ('f', 'Finalizado'),
    ]

    protocolo = models.PositiveIntegerField(
        unique=True,
        editable=False
    )

    nome = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-zÀ-ÿ\s]+$',
                message='O nome deve conter apenas letras e espaços.'
            )
        ]
    )

    email = models.EmailField(max_length=50)

    telefone = models.CharField(
    max_length=20,
    blank=True,
    default='',
    validators=[
        RegexValidator(
            regex=r'^\d+$',
            message='O telefone deve conter apenas números.'
        )
    ]
)

    endereco = models.CharField(max_length=50)
    problema = models.CharField(max_length=20)

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='p'
    )

    notas = models.CharField(
        max_length=250,
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            ultimo_servico = Servico.objects.order_by(
                '-protocolo'
            ).first()

            if ultimo_servico:
                self.protocolo = ultimo_servico.protocolo + 1
            else:
                self.protocolo = 1

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        protocolo_excluido = self.protocolo

        with transaction.atomic():
            super().delete(*args, **kwargs)

            servicos_posteriores = Servico.objects.filter(
                protocolo__gt=protocolo_excluido
            ).order_by('protocolo')

            for servico in servicos_posteriores:
                servico.protocolo -= 1
                servico.save(update_fields=['protocolo'])

    def __str__(self):
        return f'Protocolo {self.protocolo} - {self.nome}'