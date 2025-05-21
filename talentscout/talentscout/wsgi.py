import os
from django.core.wsgi import get_wsgi_application
import nltk

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentscout.settings')

application = get_wsgi_application()

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
