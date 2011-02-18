# -*- coding: utf-8 -*-

from django import forms
from meta.models import *
from django.db.models import Q

    
class SearchForm(forms.Form):
    query = forms.CharField(
            label=u'Buscar por',
            widget=forms.TextInput(attrs={'size': 32}),
            help_text=u'(digite um ou mais termos)',
            )

METAS = (
        (u'author', u'Autor'),
        (u'taxon', u'Táxon'),
        (u'size', u'Tamanho'),
        (u'sublocation', u'Local'),
        (u'city', u'Cidade'),
        (u'state', u'Estado'),
        (u'country', u'País'),
        )

class RelatedForm(forms.Form):
    type = forms.ChoiceField(choices=METAS, label=u'Navegando por')
    #TODO Incluir um checkbox para mostrar apenas highlights?

class FixTaxaForm(forms.Form):
    '''Formulário que mostra os táxons órfãos.
    
    Seleciona táxons que não tem pai, cujo ranking não é Reino, ou táxons sem 
    ranking.
    '''
    def get_orphans():
        '''Pega táxons sem parent e sem ranking.

        Faz o processamento para serem carregadas no formulário.
        '''
        taxa = Taxon.objects.filter(Q(parent__isnull=True) & ~Q(rank='Reino') | 
                Q(rank=''))
        semitaxa = [(taxon.name, u'%s (id=%s)' % (taxon.name, taxon.id)) for 
                taxon in taxa]
        orphans = tuple(semitaxa)
        return orphans

    review = forms.MultipleChoiceField(choices=get_orphans(), 
            widget=forms.CheckboxSelectMultiple(attrs={'class':'check-taxon'}), 
            required=False, label=u'Revisar táxons')
