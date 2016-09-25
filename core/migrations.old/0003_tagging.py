
from south.db import db
from django.db import models
from core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Post.tags'
        db.add_column('core_post', 'tags', orm['core.post:tags'])
        
        # Changing field 'Post.published_at'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('core_post', 'published_at', orm['core.post:published_at'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Post.tags'
        db.delete_column('core_post', 'tags')
        
        # Changing field 'Post.published_at'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('core_post', 'published_at', orm['core.post:published_at'])
        
    
    
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
