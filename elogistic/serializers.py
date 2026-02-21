from rest_framework import serializers
from .models import NetworkNode, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RublesField(serializers.Field):
    """Поле для ввода/вывода рублей, хранящее значение в копейках."""
    def to_representation(self, value):
        # value приходит из модели (в копейках)
        return value / 100.0

    def to_internal_value(self, data):
        from decimal import Decimal, ROUND_HALF_UP
        try:
            # Преобразуем в Decimal для точности
            rub = Decimal(str(data))  # str важно, чтобы не терять точность
            kopecks = (rub * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            return int(kopecks)
        except:
            raise serializers.ValidationError('Должно быть число.')

class NetworkNodeSerializer(serializers.ModelSerializer):
    debt = RublesField(required=False)
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    products_detail = ProductSerializer(source='products', many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'
        read_only_fields = ('created_at',)

    def update(self, instance, validated_data):
        # Запрещаем обновление поля debt
        validated_data.pop('debt', None)
        return super().update(instance, validated_data)
