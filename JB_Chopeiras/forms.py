from django import forms
from servicos.models import Servico


class SolicitacaoForm(forms.ModelForm):

    telefone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={ 'inputmode': 'numeric', 'pattern': '[0-9]*', 'placeholder': 'Digite apenas números' } ) )

    explicacao = forms.CharField( max_length=250, widget=forms.Textarea( attrs={ 'rows': 5 } ) )

    class Meta:
        model = Servico

        fields = [ 'nome', 'email', 'telefone', 'problema', 'endereco',]

    def clean_nome(self):
        nome = self.cleaned_data.get( 'nome', '' ).strip()

        if not nome.replace(' ', '').isalpha():
            raise forms.ValidationError( 'O nome deve conter apenas letras.' )

        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get( 'telefone', '' ).strip()

        if not telefone.isdigit():
            raise forms.ValidationError( 'O telefone deve conter apenas números.' )

        return telefone

    def clean_problema(self):
        problema = self.cleaned_data.get( 'problema', '' ).strip()

        if not problema.replace(' ', '').isalpha():
            raise forms.ValidationError( 'O problema deve conter apenas letras.' )

        return problema

    def save(self, commit=True):

        servico = super().save(commit=False)

        servico.notas = self.cleaned_data['explicacao']

        servico.status = 'p'

        if commit:
            servico.save()

        return servico