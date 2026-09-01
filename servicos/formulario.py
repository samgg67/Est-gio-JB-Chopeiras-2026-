from django import forms

from .models import Servico


class ServicoFormulario(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'nome', 'email', 'telefone', 'endereco', 'problema', 'status',
            'notas', 'quantidade', 'previsao_entrega',
        ]
        widgets = {'previsao_entrega': forms.DateInput(attrs={'type': 'date'})}

    def clean_nome(self):
        nome = self.cleaned_data.get('nome', '').strip()
        if not nome.replace(' ', '').isalpha():
            raise forms.ValidationError('O nome deve conter apenas letras e espaços.')
        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').strip()
        if telefone and not telefone.isdigit():
            raise forms.ValidationError('O telefone deve conter apenas números.')
        return telefone


class SolicitacaoFormulario(ServicoFormulario):
    explicacao = forms.CharField(
        label='Explicação',
        max_length=250,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Descreva os sintomas e quando o problema começou...',
        }),
    )

    class Meta:
        model = Servico
        fields = ['nome', 'telefone', 'problema', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={
                'autocomplete': 'name',
                'placeholder': 'Seu nome completo',
            }),
            'telefone': forms.TextInput(attrs={
                'autocomplete': 'tel',
                'inputmode': 'numeric',
                'pattern': '[0-9]*',
                'placeholder': '43999999999',
            }),
            'problema': forms.TextInput(attrs={
                'placeholder': 'Ex.: Vazamento',
            }),
            'endereco': forms.TextInput(attrs={
                'autocomplete': 'street-address',
                'placeholder': 'Rua, número e bairro',
            }),
        }

    def clean_problema(self):
        problema = self.cleaned_data.get('problema', '').strip()
        if not problema.replace(' ', '').isalpha():
            raise forms.ValidationError('O problema deve conter apenas letras.')
        return problema

    def save(self, commit=True):
        servico = super().save(commit=False)
        servico.notas = self.cleaned_data['explicacao']
        servico.status = 'p'
        if commit:
            servico.save()
        return servico
