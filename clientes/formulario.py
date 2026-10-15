from django import forms
from clientes.models import Clientes
from clientes.validadores import limpar_nome, limpar_telefone, validar_email_unico


class ClientesFormulario(forms.ModelForm):

    tempo_de_fidelidade = forms.IntegerField( required=False, min_value=0)

    servicos_realizados = forms.IntegerField( required=False, min_value=0)

    class Meta:
        model = Clientes

        fields = [ 'nome', 'email', 'telefone', 'endereco', 'tempo_de_fidelidade', 'servicos_realizados']


    def clean_nome(self):
        return limpar_nome(self.cleaned_data.get('nome'))


    def clean_email(self):
        return validar_email_unico(self.cleaned_data.get('email'), self.instance.pk)


    def clean_telefone(self):
        return limpar_telefone(self.cleaned_data.get('telefone'))


    def clean_tempo_de_fidelidade(self):
        return self.cleaned_data.get('tempo_de_fidelidade') or 0


    def clean_servicos_realizados(self):
        return self.cleaned_data.get('servicos_realizados') or 0


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
        nome = limpar_nome(self.cleaned_data.get('nome'))
        if not nome:
            raise forms.ValidationError('Informe seu nome.')
        return nome

    def clean_telefone(self):
        return limpar_telefone(self.cleaned_data.get('telefone'))
