
from south.db import db
from django.db import models
from core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Measurement'
        db.create_table('core_measurement', (
            ('id', orm['core.measurement:id']),
            ('recipe', orm['core.measurement:recipe']),
            ('ingredient', orm['core.measurement:ingredient']),
            ('amount', orm['core.measurement:amount']),
            ('unit', orm['core.measurement:unit']),
            ('order', orm['core.measurement:order']),
        ))
        db.send_create_signal('core', ['Measurement'])
        
        # Adding model 'Recipe'
        db.create_table('core_recipe', (
            ('post_ptr', orm['core.recipe:post_ptr']),
        ))
        db.send_create_signal('core', ['Recipe'])
        
        # Adding model 'Photo'
        db.create_table('core_photo', (
            ('id', orm['core.photo:id']),
            ('title', orm['core.photo:title']),
            ('image', orm['core.photo:image']),
        ))
        db.send_create_signal('core', ['Photo'])
        
        # Adding model 'Unit'
        db.create_table('core_unit', (
            ('id', orm['core.unit:id']),
            ('metric', orm['core.unit:metric']),
            ('imperial', orm['core.unit:imperial']),
            ('conversion', orm['core.unit:conversion']),
        ))
        db.send_create_signal('core', ['Unit'])
        
        # Adding model 'Ingredient'
        db.create_table('core_ingredient', (
            ('post_ptr', orm['core.ingredient:post_ptr']),
        ))
        db.send_create_signal('core', ['Ingredient'])
        
        # Adding model 'Post'
        db.create_table('core_post', (
            ('id', orm['core.post:id']),
            ('title', orm['core.post:title']),
            ('slug', orm['core.post:slug']),
            ('text', orm['core.post:text']),
            ('pic', orm['core.post:pic']),
            ('published_at', orm['core.post:published_at']),
        ))
        db.send_create_signal('core', ['Post'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Measurement'
        db.delete_table('core_measurement')
        
        # Deleting model 'Recipe'
        db.delete_table('core_recipe')
        
        # Deleting model 'Photo'
        db.delete_table('core_photo')
        
        # Deleting model 'Unit'
        db.delete_table('core_unit')
        
        # Deleting model 'Ingredient'
        db.delete_table('core_ingredient')
        
        # Deleting model 'Post'
        db.delete_table('core_post')
        
    
    
    models = {
        'core.ingredient': {
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.measurement': {
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Ingredient']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']"})
        },
        'core.photo': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'core.post': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']", 'null': 'True', 'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
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
