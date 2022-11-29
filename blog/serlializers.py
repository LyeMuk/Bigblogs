
from .models import blogg
  
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = blogg
        fields = ('bid', 'bdate', 'authorname', 'title', 'content')