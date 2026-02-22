from rest_framework import serializers
from .models import NetworkNode, Product
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import re


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class RublesField(serializers.Field):
    """
    Поле для ввода/вывода рублей с точностью до копеек.
    На вход ожидает строку вида '1234.56' или целое число (копейки не допускаются).
    В модели хранит целое число копеек.
    """
    def to_representation(self, value):
        # value — целое число копеек
        rub = Decimal(value) / 100
        # Возвращаем строку с двумя знаками после запятой (требование API)
        return f"{rub:.2f}"

    def to_internal_value(self, data):
        # Приводим к строке для дальнейшей обработки, если вдруг пользователь передал число
        str_value = str(data).strip()
        # Проверка формата: число с не более чем двумя знаками после запятой
        if str_value[:1] == '-':
            raise serializers.ValidationError(
                'Задолженность не может быть отрицательной.'
            )
        if not re.match(r'^-?\d+(\.\d{1,2})?$', str_value):
            raise serializers.ValidationError(
                'Неверный формат. Ожидается число с не более чем двумя знаками после запятой (например, "123.45").'
            )

        try:
            rub = Decimal(str_value)
            # Умножаем на 100 и округляем до целого по правилу "половина вверх"
            kopecks = (rub * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            return int(kopecks)
        except (InvalidOperation, ValueError):
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
