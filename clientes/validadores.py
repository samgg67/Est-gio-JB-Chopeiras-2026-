import re

from django.core.exceptions import ValidationError
from django.utils import timezone

from clientes.models import Clientes


def limpar_nome(valor):
    nome = ' '.join((valor or '').split())
    if not nome:
        return nome

    if not all(caractere.isalpha() or caractere == ' ' for caractere in nome):
        raise ValidationError('O nome deve conter apenas letras e espaços.')

    if sum(caractere.isalpha() for caractere in nome) < 2:
        raise ValidationError('Informe um nome válido.')

    return nome


def validar_email_unico(valor, cliente_id=None):
    email = (valor or '').strip().lower()
    if not email:
        return email

    existente = Clientes.objects.filter(email__iexact=email).exclude(pk=cliente_id).first()
    if existente:
        if existente.deletado_em:
            raise ValidationError(
                f'Já existe um cliente inativo com esse e-mail ({existente.nome}). Reative o cadastro dele.'
            )
        raise ValidationError(f'Já existe um cliente com esse e-mail ({existente.nome}).')

    return email


def limpar_problema(valor):
    problema = ' '.join((valor or '').split())
    if not problema:
        return problema

    permitidos = set('/-,. ')
    if not all(caractere.isalpha() or caractere in '0123456789' or caractere in permitidos for caractere in problema):
        raise ValidationError('O problema pode ter apenas letras, números, espaços e / - , .')

    if not any(caractere.isalpha() for caractere in problema):
        raise ValidationError('Descreva o problema com palavras.')

    return problema


def validar_previsao_entrega(data):
    if data and data < timezone.localdate():
        raise ValidationError('A previsão de entrega não pode ser uma data que já passou.')
    return data


def limpar_telefone(valor):
    telefone = (valor or '').strip()
    if not telefone:
        return telefone

    if re.search(r'[^0-9\s()+\-.]', telefone):
        raise ValidationError('O telefone deve conter apenas números.')

    numeros = re.sub(r'[^0-9]', '', telefone)
    if len(numeros) in (12, 13) and numeros.startswith('55'):
        numeros = numeros[2:]

    if len(numeros) not in (10, 11):
        raise ValidationError('Informe um telefone válido com DDD (10 ou 11 números).')

    return numeros
