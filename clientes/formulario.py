from django import forms
from clientes.models import Clientes
import re


class ClientesFormulario(forms.ModelForm):

    tempo_de_fidelidade = forms.IntegerField( required=False)

    servicos_realizados = forms.IntegerField( required=False)

    class Meta:
        model = Clientes

        fields = [ 'nome', 'email', 'telefone', 'endereco', 'tempo_de_fidelidade', 'servicos_realizados']


    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if not nome:
            return nome

        if not re.fullmatch(r'[A-Za-zÀ-ÿ\s]+', nome):
            raise forms.ValidationError( 'O nome deve conter apenas letras e espaços.' )

        return nome


    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        if not telefone:
            return telefone

        if not telefone.isdigit():
            raise forms.ValidationError( 'O telefone deve conter apenas números.')

        return telefone


class PerfilClienteFormulario(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nome', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'autocomplete': 'name'}),
            'telefone': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'endereco': forms.TextInput(attrs={'autocomplete': 'street-address'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if not nome:
            raise forms.ValidationError('Informe seu nome.')
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        numeros = re.sub(r'\D', '', telefone)
        if len(numeros) < 10 or len(numeros) > 11:
            raise forms.ValidationError('Informe um telefone válido com DDD.')
        return telefone
