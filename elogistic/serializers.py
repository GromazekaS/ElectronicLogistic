from rest_framework import serializers
from .models import NetworkNode, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    # Для вывода задолженности в рублях (строка с двумя знаками)
    debt = serializers.SerializerMethodField()
    # Для записи продуктов используем список id, для чтения добавляем детальную информацию
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    products_detail = ProductSerializer(source='products', many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'
        read_only_fields = ('created_at',)  # поле created_at не редактируется

    def get_debt(self, obj):
        """Преобразует копейки в рубли с двумя знаками."""
        return f"{obj.debt / 100:.2f}"

    def to_internal_value(self, data):
        """
        Преобразует входные данные перед валидацией.
        Перехватываем поле 'debt' и переводим рубли в копейки.
        """
        # Создаём копию, так как data может быть неизменяемым (например, QueryDict)
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)

        debt_rub = data_copy.get('debt')
        if debt_rub is not None:
            try:
                # Преобразуем в число с плавающей точкой, затем в копейки
                # Предполагаем, что может прийти как строка, так и число
                rub = float(debt_rub)
                kopecks = int(round(rub * 100))  # round для избежания ошибок округления
                data_copy['debt'] = kopecks
            except (ValueError, TypeError):
                raise serializers.ValidationError({'debt': 'Неверный формат задолженности. Ожидается число.'})

        return super().to_internal_value(data_copy)

    def update(self, instance, validated_data):
        """
        Запрещаем изменение поля debt при обновлении.
        """
        validated_data.pop('debt', None)  # удаляем, если вдруг пришло
        return super().update(instance, validated_data)
