# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-02 22:19
from __future__ import unicode_literals
from tqdm import tqdm

from django.db import migrations, models

from seqr.utils.xpos_utils import get_chrom_pos

CN_MAP = {0: 2, 1: 1, 2: 0}
DUP_CN_MAP = {0: 2, 1: 3, 2: 4}


def update_saved_variants(apps, schema_editor):
    SavedVariant = apps.get_model("seqr", "SavedVariant")
    db_alias = schema_editor.connection.alias
    variants = SavedVariant.objects.using(db_alias).all()
    if variants:
        print('Updating  {} variants'.format(len(variants)))
        for variant in tqdm(variants, unit=' variants'):
            if variant.ref == 'X':
                # Migrate manually created variants
                variant.ref = None
                variant.alt = None
                pos_end = variant.saved_variant_json.pop('pos_end', None)
                if pos_end:
                    variant.saved_variant_json['end'] = pos_end
                for genotype in variant.saved_variant_json['genotypes'].values():
                    cn_map = DUP_CN_MAP if variant.saved_variant_json['svType'] == 'DUP' else CN_MAP
                    num_alt = genotype.pop('numAlt')
                    genotype['cn'] = cn_map[num_alt]
            variant_id = variant.saved_variant_json.get('variantId')
            if not variant_id:
                if not variant.ref:
                    raise Exception('Invalid variant {}'.format(variant.guid))
                chrom, pos = get_chrom_pos(variant.xpos_start)
                variant_id = '{}-{}-{}-{}'.format(chrom, pos, variant.ref, variant.alt)
            variant.variant_id = variant_id
            variant.save()


def update_saved_search_datset_type(apps, schema_editor):
    VariantSearch = apps.get_model("seqr", "VariantSearch")
    db_alias = schema_editor.connection.alias
    saved_searches = VariantSearch.objects.using(db_alias).exclude(name__isnull=True)
    if saved_searches:
        print('Updating  {} searches'.format(len(saved_searches)))
        for search in tqdm(saved_searches, unit=' searches'):
            search.search['datasetType'] = 'VARIANTS'
            search.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('seqr', '0008_auto_20200317_1716'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedvariant',
            name='variant_id',
            field=models.TextField(default='X', db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sample',
            name='sample_type',
            field=models.CharField(choices=[(b'WES', b'Exome'), (b'WGS', b'Whole Genome'), (b'RNA', b'RNA')], max_length=10),
        ),
        migrations.AlterField(
            model_name='savedvariant',
            name='alt',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='savedvariant',
            name='ref',
            field=models.TextField(null=True),
        ),
        migrations.RunPython(update_saved_variants, reverse_code=migrations.RunPython.noop),
        migrations.RunPython(update_saved_search_datset_type, reverse_code=migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name='savedvariant',
            unique_together=set([('xpos_start', 'xpos_end', 'variant_id', 'family')]),
        ),
    ]
