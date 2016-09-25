
from south.db import db
from django.db import models
from core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Measurement.detail'
        db.add_column('core_measurement', 'detail', orm['core.measurement:detail'])
        
        # Changing field 'Measurement.unit'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['core.Unit'], null=True, blank=True))
        db.alter_column('core_measurement', 'unit_id', orm['core.measurement:unit'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Measurement.detail'
        db.delete_column('core_measurement', 'detail')
        
        # Changing field 'Measurement.unit'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['core.Unit']))
        db.alter_column('core_measurement', 'unit_id', orm['core.measurement:unit'])
        
    
    
    models = {
        'core.ingredient': {
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.measurement': {
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Ingredient']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']", 'null': 'True', 'blank': 'True'})
        },
        'core.photo': {
            'author': ('django.db.models.fields.CharField', [], {'default': "'Adriano'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.post': {
            'author': ('django.db.models.fields.CharField', [], {'default': "'Adriano'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']", 'null': 'True', 'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tags': ('TagField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.recipe': {
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.unit': {
            'conversion': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imperial': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'metric': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['core']
