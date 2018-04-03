# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-03-26 20:31
from __future__ import unicode_literals
import re

from django.conf import settings
from django.db import migrations, models
from django.utils.text import slugify

class Migration(migrations.Migration):
    def unmangle_identifier(apps, schema_editor):
        '''
        The `fix_bill_id` function mangled bill identifiers in at least two ways:
        (1) removing zeroes, e.g., 'Res 0229-2004' (original) becomes 'Res 229-2004' (mangled)
        (2) adding a space, e.g., 'T2018-1245' (original) becomes 'T 2018-1245' (mangled).

        For NYC, the second case ONLY affected bills that begin with 'T', and the first case did NOT affect bills that begin with 'T' - that is, NYC bills never follow these patterns 'T 0023-2015' or 'T0023-2015'.

        This migration unmangles identifiers and changes the slugs accordingly.
        '''

        Bill = apps.get_model('councilmatic_core', 'Bill')

        # New York City
        if settings.OCD_CITY_COUNCIL_ID == 'ocd-organization/0f63aae8-16fd-4d3c-b525-00747a482cf9':
            deleted_zeroes = r'^((?!T\s)[A-Za-z]+)\s(\d{1,3})-([-\w]+)$'
            for bill in Bill.objects.filter(identifier__iregex=deleted_zeroes):
                match = re.match(deleted_zeroes, bill.identifier)
                unmangled_identifier = '{prefix} {mangled_count:0>4}-{remainder}'.format(prefix=match.group(1), 
                                                                                         mangled_count=match.group(2),
                                                                                         remainder=match.group(3))

                print('{} becomes {}'.format(bill.identifier, unmangled_identifier))
                try:
                    duplicate = Bill.objects.get(identifier=unmangled_identifier)
                    print('{} - duplicate found. Deleting.'.format(unmangled_identifier))
                    duplicate.delete()
                except Bill.DoesNotExist: 
                    pass

                bill.identifier = unmangled_identifier
                bill.slug = slugify(unmangled_identifier)
                bill.save()

            added_space = r'^(T)\s([-\d]+)$'
            for bill in Bill.objects.filter(identifier__iregex=added_space):
                match = re.match(added_space, bill.identifier)
                unmangled_identifier = '{mangled_prefix}{count}'.format(mangled_prefix=match.group(1), 
                                                                        count=match.group(2))
                
                print('{} becomes {}'.format(bill.identifier, unmangled_identifier))
                try:
                    duplicate = Bill.objects.get(identifier=unmangled_identifier)
                    print('{} - duplicate found. Deleting.'.format(unmangled_identifier))
                    duplicate.delete()
                except Bill.DoesNotExist: 
                    pass

                bill.identifier = unmangled_identifier
                bill.slug = slugify(unmangled_identifier)
                bill.save()
                
    dependencies = [
        ('councilmatic_core', '0036_auto_20180302_1247'),
    ]

    operations = [
        migrations.RunPython(unmangle_identifier)
    ]
