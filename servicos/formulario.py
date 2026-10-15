from django import forms
from django.utils import timezone

from clientes.validadores import (
    limpar_nome,
    limpar_problema,
    limpar_telefone,
    validar_previsao_entrega,
)

from .models import Servico


class ServicoFormulario(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'nome', 'email', 'telefone', 'endereco', 'problema', 'status',
            'notas', 'quantidade', 'previsao_entrega',
        ]
        widgets = {'previsao_entrega': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'previsao_entrega' in self.fields:
            minimo = timezone.localdate()
            salva = self.instance.previsao_entrega
            if salva and salva < minimo:
                minimo = salva
            self.fields['previsao_entrega'].widget.attrs['min'] = minimo.isoformat()

    def clean_nome(self):
        return limpar_nome(self.cleaned_data.get('nome'))

    def clean_telefone(self):
        return limpar_telefone(self.cleaned_data.get('telefone'))

    def clean_problema(self):
        return limpar_problema(self.cleaned_data.get('problema'))

    def clean_previsao_entrega(self):
        previsao = self.cleaned_data.get('previsao_entrega')
        # Ao editar, uma data antiga que já estava salva continua valendo.
        if 'previsao_entrega' in self.changed_data:
            validar_previsao_entrega(previsao)
        return previsao

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is not None and quantidade < 1:
            raise forms.ValidationError('A quantidade deve ser pelo menos 1.')
        return quantidade


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefone'].required = True

    def save(self, commit=True):
        servico = super().save(commit=False)
        servico.notas = self.cleaned_data['explicacao']
        servico.status = 'p'
        if commit:
            servico.save()
        return servico
