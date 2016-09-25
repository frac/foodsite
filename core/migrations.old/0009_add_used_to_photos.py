
from south.db import db
from django.db import models
from foodsite.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Photo.used'
        db.add_column('core_photo', 'used', orm['core.photo:used'])
        
        # Creating unique_together for [slug] on Post.
        #db.create_unique('core_post', ['slug'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [slug] on Post.
        db.delete_unique('core_post', ['slug'])
        
        # Deleting field 'Photo.used'
        db.delete_column('core_photo', 'used')
        
    
    
    models = {
        'core.ingredient': {
            'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['core.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        'core.measurement': {
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Ingredient']", 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Recipe']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Unit']", 'null': 'True', 'blank': 'True'})
        },
        'core.photo': {
            'author': ('django.db.models.fields.CharField', [], {'default': "'Adriano'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'core.post': {
            'author': ('django.db.models.fields.CharField', [], {'default': "'Adriano'", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Photo']", 'null': 'True', 'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
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
