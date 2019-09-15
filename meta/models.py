# -*- coding: utf-8 -*-

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel
from meta.signals import *
from django.db.models import Q
from django.db.models import signals


class Media(models.Model):
    '''Table containing both image and video files.'''

    # File
    filepath = models.CharField(_('arquivo original.'), max_length=200,
            unique=True, help_text=_('Caminho único para arquivo original.'))
    sitepath = models.FileField(_('arquivo web.'), unique=True,
            help_text=_('Arquivo processado para a web.'))
    coverpath = models.ImageField(_('amostra do arquivo.'), unique=True,
            help_text=_('Imagem de amostra do arquivo processado.'))
    datatype = models.CharField(_('tipo de mídia'), max_length=15,
            help_text=_('Tipo de mídia.'))
    timestamp = models.DateTimeField(_('data de modificação'),
            help_text=_('Data da última modificação do arquivo.'))

    # Website
    old_image = models.PositiveIntegerField(default=0, blank=True,
            help_text=_('ID da imagem no antigo modelo.'))
    old_video = models.PositiveIntegerField(default=0, blank=True,
            help_text=_('ID do vídeo no antigo modelo.'))
    highlight = models.BooleanField(_('destaque'), default=False,
            help_text=_('Imagem que merece destaque.'))
    is_public = models.BooleanField(_('público'), default=False,
            help_text=_('Visível para visitantes.'))
    pub_date = models.DateTimeField(_('data de publicação'), auto_now_add=True,
            help_text=_('Data de publicação da imagem no Cifonauta.'))

    # Metadata
    title = models.CharField(_('título'), max_length=200, default='',
            blank=True, help_text=_('Título da imagem.'))
    caption = models.TextField(_('legenda'), default='', blank=True,
            help_text=_('Legenda da imagem.'))
    date = models.DateTimeField(_('data'), null=True, blank=True,
            help_text=_('Data de criação da imagem.'))
    geolocation = models.CharField(_('geolocalização'), default='',
            max_length=25, blank=True,
            help_text=_('Geolocalização da imagem no formato decimal.'))
    latitude = models.CharField(_('latitude'), default='', max_length=25,
            blank=True, help_text=_('Latitude onde a imagem foi criada.'))
    longitude = models.CharField(_('longitude'), default='', max_length=25,
            blank=True, help_text=_('Longitude onde a imagem foi criada.'))
    duration = models.CharField(_('duração'), max_length=20,
            default='00:00:00', blank=True,
            help_text=_('Duração do vídeo no formato HH:MM:SS.'))
    dimensions = models.CharField(_('dimensões'), max_length=20, default='0x0',
            blank=True, help_text=_('Dimensões do vídeo original.'))

    # Foreign metadata
    size = models.ForeignKey('Size', on_delete=models.SET_NULL, null=True,
            blank=True, verbose_name=_('tamanho'),
            help_text=_('Classe de tamanho do organismo na imagem.'))
    sublocation = models.ForeignKey('Sublocation', on_delete=models.SET_NULL,
            null=True, blank=True, verbose_name=_('local'),
            help_text=_('Localidade mostrada na imagem (ou local de coleta).'))
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True,
            blank=True, verbose_name=_('cidade'),
            help_text=_('Cidade mostrada na imagem (ou cidade de coleta).'))
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True,
            blank=True, verbose_name=_('estado'),
            help_text=_('Estado mostrado na imagem (ou estado de coleta).'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL,
            null=True, blank=True, verbose_name=_('país'),
            help_text=_('País mostrado na imagem (ou país de coleta).'))

    def __str__(self):
        return 'ID={} {} ({})'.format(self.id, self.title, self.datatype)

    def get_absolute_url(self):
        return reverse('media_url', args=[str(self.id)])

    class Meta:
        verbose_name = _('arquivo')
        verbose_name_plural = _('arquivos')
        ordering = ['id']


class Person(models.Model):
    name = models.CharField(_('nome'), max_length=200, unique=True, blank=True,
            help_text=_('Nome do autor.'))
    slug = models.SlugField(_('slug'), max_length=200, unique=True, blank=True,
            help_text=_('Slug do nome do autor.'))
    is_author = models.BooleanField(_('author'), default=False,
            help_text=_('Informa se a pessoa é autora.'))
    media = models.ManyToManyField('Media', blank=True,
            verbose_name=_('fotos'),
            help_text=_('Arquivos associados a este autor.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person_url', args=[self.slug])

    class Meta:
        verbose_name = _('pessoa')
        verbose_name_plural = _('pessoas')
        ordering = ['name']


class File(models.Model):
    '''Define campos comuns para arquivos de mídia.'''
    # File
    filename = models.CharField(_(u'Nome único do arquivo.'), max_length=200,
            blank=True, help_text=_(u'Nome único e identificador do arquivo.'))
    filepath = models.ImageField(_(u'arquivo fonte local (novo)'), default='',
            upload_to='site_media/photos/', null=True, blank=True, help_text=_(u'Arquivo na pasta do site.'))
    source_filepath = models.CharField(_(u'arquivo fonte local'),
            max_length=200, blank=True, help_text=_(u'Arquivo fonte na pasta local.'))
    thumb_filepath = models.ImageField(_(u'thumbnail web'),
            upload_to='site_media/images/thumbs', help_text=_(u'Pasta que guarda thumbnails.'))
    old_filepath = models.CharField(_(u'arquivo fonte original'),
            max_length=200, blank=True, help_text=_(u'Caminho para o arquivo original.'))
    timestamp = models.DateTimeField(_(u'data de modificação'),
            help_text=_(u'Data da última modificação do arquivo.'))

    # Website
    highlight = models.BooleanField(_(u'destaque'), default=False, help_text=_(u'Imagem que merece destaque.'))
    cover = models.BooleanField(_(u'imagem de capa'), default=False, help_text=_(u'Imagem esteticamente bela, para usar na página principal.'))
    is_public = models.BooleanField(_(u'público'), default=False, help_text=_(u'Informa se imagem está visível para visitantes anônimos do site.'))
    pub_date = models.DateTimeField(_(u'data de publicação'), auto_now_add=True, help_text=_(u'Data de publicação da imagem no Cifonauta.'))

    # IPTC
    title = models.CharField(_(u'título'), max_length=200, blank=True, help_text=_(u'Título da imagem.'))
    caption = models.TextField(_(u'legenda'), blank=True, help_text=_(u'Legenda da imagem.'))
    #NOTA null e blank devem ser True
    # null está se referindo ao NULL do banco de dados e
    # blank está se referindo à interface de admin.
    size = models.ForeignKey('Size', null=True, blank=True, default='',
            verbose_name=_(u'tamanho'), help_text=_(u'Classe de tamanho do organismo na imagem.'), on_delete=models.DO_NOTHING)
    sublocation = models.ForeignKey('Sublocation', null=True, blank=True,
            verbose_name=_(u'local'), help_text=_(u'Localidade mostrada na imagem (ou local de coleta).'), on_delete=models.DO_NOTHING)
    city = models.ForeignKey('City', null=True, blank=True, verbose_name=('cidade'), help_text=_(u'Cidade mostrada na imagem (ou cidade de coleta).'), on_delete=models.DO_NOTHING)
    state = models.ForeignKey('State', null=True, blank=True, verbose_name=_(u'estado'), help_text=_(u'Estado mostrado na imagem (ou estado de coleta).'), on_delete=models.DO_NOTHING)
    country = models.ForeignKey('Country', null=True, blank=True, verbose_name=_(u'país'), help_text=_(u'País mostrado na imagem (ou país de coleta).'), on_delete=models.DO_NOTHING)

    # EXIF
    date = models.DateTimeField(_(u'data'), blank=True, help_text=_(u'Data em que a imagem foi criada.'))
    geolocation = models.CharField(_(u'geolocalização'), max_length=25,
            blank=True, help_text=_(u'Geolocalização da imagem no formato decimal.'))
    latitude = models.CharField(_(u'latitude'), max_length=12, blank=True, help_text=_(u'Latitude onde foi criada a imagem.'))
    longitude = models.CharField(_(u'longitude'), max_length=12, blank=True, help_text=_(u'Longitude onde foi criada a imagem.'))

    class Meta:
        abstract = True
        verbose_name = _(u'arquivo')
        verbose_name_plural = _(u'arquivos')

    def _get_list(self, obj_set, field_name="name", lang=False, separator=' , '):
        if lang:
            name = "%s_%s" % (field_name, lang)
        else:
            name = field_name
        results = []
        return separator.join(obj_set.values_list(name, flat=True))

    def get_authors_list(self, separator=','):
        return self._get_list(self.author_set, separator=separator)

    def get_sources_list(self, separator=','):
        return self._get_list(self.source_set, separator=separator)

    def get_tag_list_pt(self):
        return self._get_list(self.tag_set, lang='pt_br')

    def get_tag_list_en(self):
        return self._get_list(self.tag_set, lang='en')

    def get_taxon_name_list_no_parents(self):
        return str(self.taxon_set.values_list('pk', flat=True))[1:-1]

    def get_taxon_name_list(self):
        return self._get_list(Taxon.get_taxon_and_parents(self.taxon_set))

    def get_taxon_common_list_pt(self):
        return self._get_list(Taxon.get_taxon_and_parents(self.taxon_set), field_name='common', lang='pt_br')

    def get_taxon_common_list_en(self):
        return self._get_list(Taxon.get_taxon_and_parents(self.taxon_set), field_name='common', lang='en')

    def get_taxon_rank_list_pt(self):
        return self._get_list(self.taxon_set, field_name='rank', lang='pt_br')

    def get_taxon_rank_list_en(self):
        return self._get_list(self.taxon_set, field_name='rank', lang='en')


class Image(File):
    web_filepath = models.ImageField(_(u'arquivo web'),
            upload_to='site_media/images/', help_text=_(u'Caminho para o arquivo web.'))
    datatype = models.CharField(_(u'tipo de mídia'), max_length=10,
            default='photo', help_text=_(u'Tipo de mídia.'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('image_url', [str(self.id)])

    class Meta:
        verbose_name = _(u'foto')
        verbose_name_plural = _(u'fotos')
        ordering = ['id']


class Video(File):
    webm_filepath = models.FileField(_(u'arquivo webm'),
            upload_to='site_media/videos/', blank=True, help_text=_(u'Caminho para o arquivo WEBM.'))
    ogg_filepath = models.FileField(_(u'arquivo ogg'),
            upload_to='site_media/videos/', blank=True, help_text=_(u'Caminho para o arquivo OGG.'))
    mp4_filepath = models.FileField(_(u'arquivo mp4'),
            upload_to='site_media/videos/', blank=True, help_text=_(u'Caminho para o arquivo MP4.'))
    datatype = models.CharField(_(u'tipo de mídia'), max_length=10,
            default='video', help_text=_(u'Tipo de mídia.'))
    large_thumb = models.ImageField(_(u'thumbnail grande'),
            upload_to='site_media/images/thumbs', help_text=_(u'Caminho para o thumbnail grande do vídeo.'))
    duration = models.CharField(_(u'duração'), max_length=20,
            default='00:00:00', help_text=_(u'Duração do vídeo no formato HH:MM:SS.'))
    dimensions = models.CharField(_(u'dimensões'), max_length=20, default='0x0', help_text=_(u'Dimensões do vídeo original.'))
    codec = models.CharField(_(u'codec'), max_length=20, default='', help_text=_(u'Codec do vídeo original.'))

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('video_url', [str(self.id)])

    class Meta:
        verbose_name = _(u'vídeo')
        verbose_name_plural = _(u'vídeos')
        ordering = ['id']


class Author(models.Model):
    name = models.CharField(_(u'nome'), max_length=200, unique=True, help_text=_(u'Nome do autor.'))
    slug = models.SlugField(_(u'slug'), max_length=200, blank=True, help_text=_(u'Slug do nome do autor.'))
    images = models.ManyToManyField(Image, blank=True,
            verbose_name=_(u'fotos'), help_text=_(u'Fotos associadas a este autor.'))
    videos = models.ManyToManyField(Video, blank=True,
            verbose_name=_(u'vídeos'), help_text=_(u'Vídeos associados a este autor.'))
    image_count = models.PositiveIntegerField(_(u'número de fotos'), default=0,
            editable=False, help_text=_(u'Número de fotos associadas a este autor.'))
    video_count = models.PositiveIntegerField(_(u'número de vídeos'), default=0, editable=False, help_text=_(u'Número de vídeos associados a este autor.'))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('author_url', [self.slug])

    def counter(self):
        '''Conta o número de imagens+vídeos associados.

        Atualiza os respectivos campos image_count e video_count.
        '''
        self.image_count = self.images.count()
        self.video_count = self.videos.count()
        self.save()

    class Meta:
        verbose_name = _(u'autor')
        verbose_name_plural = _(u'autores')
        ordering = ['name']


class Source(models.Model):
    name = models.CharField(_(u'nome'), max_length=200, unique=True, help_text=_(u'Nome do especialista.'))
    slug = models.SlugField(_(u'slug'), max_length=200, blank=True, help_text=_(u'Slug do nome do especialista.'))
    images = models.ManyToManyField(Image, blank=True,
            verbose_name=_(u'fotos'), help_text=_(u'Fotos associadas a este especialista.'))
    videos = models.ManyToManyField(Video, blank=True,
            verbose_name=_(u'vídeos'), help_text=_(u'Vídeos associados a este especialista.'))
    image_count = models.PositiveIntegerField(_(u'número de fotos'), default=0,
            editable=False, help_text=_(u'Número de fotos associadas a este especialista.'))
    video_count = models.PositiveIntegerField(_(u'número de vídeos'), default=0, editable=False, help_text=_(u'Número de vídeos associados a este especialista.'))

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ('source_url', [self.slug])

    def counter(self):
        '''Conta o número de imagens+vídeos associados.

        Atualiza os respectivos campos image_count e video_count.
        '''
        self.image_count = self.images.count()
        self.video_count = self.videos.count()
        self.save()

    class Meta:
        verbose_name = _(u'especialista')
        verbose_name_plural = _(u'especialistas')
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(_('nome'), max_length=64, unique=True,
            help_text=_('Nome do marcador.'))
    slug = models.SlugField(_('slug'), max_length=64, default='', blank=True,
            help_text=_('Slug do nome do marcador.'))
    description = models.TextField(_('descrição'), default='', blank=True,
            help_text=_('Descrição do marcador.'))
    media = models.ManyToManyField('Media', blank=True,
            verbose_name=_('fotos'),
            help_text=_('Fotos associadas a este marcador.'))
    parent = models.ForeignKey('TagCategory', on_delete=models.SET_NULL,
            null=True, blank=True, related_name='tags',
            verbose_name=_('categoria'),
            help_text=_('Categoria a que este marcador pertence.'))

    # Deprecated
    images = models.ManyToManyField(Image, blank=True,
            verbose_name=_(u'fotos'), help_text=_(u'Fotos associadas a este marcador.'))
    videos = models.ManyToManyField(Video, blank=True,
            verbose_name=_(u'vídeos'), help_text=_(u'Vídeos associados a este marcador.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_url', args=[self.slug])

    class Meta:
        verbose_name = _('marcador')
        verbose_name_plural = _('marcadores')
        ordering = ['name']


class TagCategory(models.Model):
    name = models.CharField(_('nome'), max_length=64, unique=True,
            help_text=_('Nome da categoria de marcadores.'))
    slug = models.SlugField(_('slug'), max_length=64, default='', blank=True,
            help_text=_('Slug do nome da categoria de marcadores.'))
    description = models.TextField(_('descrição'), default='', blank=True,
            help_text=_('Descrição da categoria de marcadores.'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('categoria de marcadores')
        verbose_name_plural = _('categorias de marcadores')
        ordering = ['name']


class Taxon(MPTTModel):
    name = models.CharField(_('nome'), max_length=256, unique=True,
            help_text=_('Nome do táxon.'))
    slug = models.SlugField(_('slug'), max_length=256, blank=True,
            help_text=_('Slug do nome do táxon.'))
    rank = models.CharField(_(u'rank'), max_length=256, blank=True, help_text=_(u'Ranking taxonômico do táxon.'))
    aphia = models.PositiveIntegerField(null=True, blank=True,
            help_text=_('APHIA, o identificador do táxon no WoRMS.'))
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True,
            null=True, related_name='children', verbose_name=_('pai'),
            help_text=_('Táxon pai deste táxon.'))
    media = models.ManyToManyField( 'Media', blank=True,
            verbose_name=_('fotos'),
            help_text=_('Fotos associadas a este táxon.'))
    timestamp = models.DateTimeField( _('data de modificação'), blank=True,
            null=True, help_text=_('Data da última modificação do arquivo.'))

    # Deprecated
    images = models.ManyToManyField(Image, blank=True,
            verbose_name=_(u'fotos'), help_text=_(u'Fotos associadas a este táxon.'))
    videos = models.ManyToManyField(Video, blank=True,
            verbose_name=_(u'vídeos'), help_text=_(u'Vídeos associados a este táxon.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('taxon_url', args=[self.slug])

    @staticmethod
    def get_taxon_and_parents(qs):
        '''Returns all parents and current taxon from a QuerySet of taxons.'''
        tree_list = {}
        query = Q()

        for node in qs.all():
            if node.tree_id not in tree_list:
                tree_list[node.tree_id] = []

            parent = node.parent.pk if node.parent is not None else None,

            if parent not in tree_list[node.tree_id]:
                tree_list[node.tree_id].append(parent)

                query |= Q(lft__lt=node.lft, rght__gt=node.rght, tree_id=node.tree_id)
            query |= Q(id=node.id)
        return Taxon.objects.filter(query)

    class Meta:
        verbose_name = _('táxon')
        verbose_name_plural = _('táxons')
        ordering = ['name']


class Size(models.Model):

    NANO = '<0,1 mm'
    MICRO = '0,1 - 1,0 mm'
    MILI = '1,0 - 10 mm'
    CENTI = '10 - 100 mm'
    MACRO = '>100 mm'
    
    SIZE_CHOICES = [
            (NANO, '<0,1 mm'),
            (MICRO, '0,1 - 1,0 mm'),
            (MILI, '1,0 - 10 mm'),
            (CENTI, '10 - 100 mm'),
            (MACRO, '>100 mm')
            ]

    name = models.CharField(_('nome'), max_length=32, unique=True,
            choices=SIZE_CHOICES, help_text=_('Nome da classe de tamanho.'))
    slug = models.SlugField(_('slug'), max_length=32, blank=True,
            help_text=_('Slug do nome da classe de tamanho.'))
    description = models.TextField(_('descrição'), blank=True,
            help_text=_('Descrição da classe de tamanho.'))

    # Deprecated
    position = models.PositiveIntegerField(_('posição'), default=0,
            help_text=_('Define ordem das classes de tamanho em um queryset.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('size_url', args=[self.slug])

    class Meta:
        verbose_name = _('tamanho')
        verbose_name_plural = _('tamanhos')
        ordering = ['position']


class Sublocation(models.Model):
    name = models.CharField(_('nome'), max_length=64, unique=True,
            help_text=_('Nome da localidade.'))
    slug = models.SlugField(_('slug'), max_length=64, blank=True,
            help_text=_('Slug do nome da localidade.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sublocation_url', args=[self.slug])

    class Meta:
        verbose_name = _('local')
        verbose_name_plural = _('locais')
        ordering = ['name']


class City(models.Model):
    name = models.CharField(_('nome'), max_length=64, unique=True,
            help_text=_('Nome da cidade.'))
    slug = models.SlugField(_('slug'), max_length=64, blank=True,
            help_text=_('Slug do nome da cidade.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city_url', args=[self.slug])

    class Meta:
        verbose_name = _('cidade')
        verbose_name_plural = _('cidades')
        ordering = ['name']


class State(models.Model):
    name = models.CharField(_('nome'), max_length=64, unique=True,
            help_text=_('Nome do estado.'))
    slug = models.SlugField(_('slug'), max_length=64, blank=True,
            help_text=_('Slug do nome do estado.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('state_url', args=[self.slug])

    class Meta:
        verbose_name = _('estado')
        verbose_name_plural = _('estados')
        ordering = ['name']


class Country(models.Model):
    name = models.CharField(_('nome'), max_length=64, unique=True,
            help_text=_('Nome do país.'))
    slug = models.SlugField(_('slug'), max_length=64, blank=True,
            help_text=_('Slug do nome do país.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country_url', args=[self.slug])

    class Meta:
        verbose_name = _('país')
        verbose_name_plural = _('país')
        ordering = ['name']


class Reference(models.Model):
    name = models.CharField(_('nome'), max_length=100, unique=True,
            help_text=_('Identificador da referência (Mendeley ID).'))
    slug = models.SlugField(_('slug'), max_length=100, blank=True,
            help_text=_('Slug do identificar da referência.'))
    citation = models.TextField(_('citação'), blank=True,
            help_text=_('Citação formatada da referência.'))
    media = models.ManyToManyField('Media', blank=True,
            verbose_name=_('fotos'),
            help_text=_('Fotos associadas à esta referência.'))

    # Deprecated
    images = models.ManyToManyField(Image, blank=True,
            verbose_name=_(u'fotos'), help_text=_(u'Fotos associadas à esta referência.'))
    videos = models.ManyToManyField(Video, blank=True,
            verbose_name=_(u'vídeos'), help_text=_(u'Vídeos associados à esta referência.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('reference_url', args=[self.slug])

    class Meta:
        verbose_name = _('referência')
        verbose_name_plural = _('referências')
        ordering = ['-citation']


class Tour(models.Model):
    name = models.CharField(_('nome'), max_length=100, unique=True,
            help_text=_('Nome do tour.'))
    slug = models.SlugField(_('slug'), max_length=100, blank=True,
            help_text=_('Slug do nome do tour.'))
    description = models.TextField(_('descrição'), blank=True,
            help_text=_('Descrição do tour.'))
    is_public = models.BooleanField(_('público'), default=False,
            help_text=_('Informa se o tour está visível para visitantes anônimos.'))
    pub_date = models.DateTimeField(_('data de publicação'), auto_now_add=True,
            help_text=_('Data de publicação do tour no Cifonauta.'))
    timestamp = models.DateTimeField(_('data de modificação'), auto_now=True,
            help_text=_('Data da última modificação do tour.'))
    media = models.ManyToManyField('Media', blank=True,
            verbose_name=_('arquivos'), help_text=_('Arquivos associadas a este tour.'))
    references = models.ManyToManyField('Reference', blank=True,
            verbose_name=_('referências'), help_text=_('Referências associadas a este tour.'))

    # Deprecated
    images = models.ManyToManyField(Image, blank=True,
            verbose_name=_(u'fotos'), help_text=_(u'Fotos associadas a este tour.'))
    videos = models.ManyToManyField(Video, blank=True,
            verbose_name=_(u'vídeos'), help_text=_(u'Vídeos associados a este tour.'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tour_url', args=[self.slug])

    class Meta:
        verbose_name = _('tour')
        verbose_name_plural = _('tours')
        ordering = ['name']


# Slugify before saving.
signals.pre_save.connect(slug_pre_save, sender=Author)
signals.pre_save.connect(slug_pre_save, sender=Tag)
signals.pre_save.connect(slug_pre_save, sender=TagCategory)
signals.pre_save.connect(slug_pre_save, sender=Taxon)
signals.pre_save.connect(slug_pre_save, sender=Size)
signals.pre_save.connect(slug_pre_save, sender=Source)
signals.pre_save.connect(slug_pre_save, sender=Sublocation)
signals.pre_save.connect(slug_pre_save, sender=City)
signals.pre_save.connect(slug_pre_save, sender=State)
signals.pre_save.connect(slug_pre_save, sender=Country)
signals.pre_save.connect(slug_pre_save, sender=Reference)
signals.pre_save.connect(slug_pre_save, sender=Tour)

# Create citation with bibkey.
signals.pre_save.connect(citation_pre_save, sender=Reference)
