from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    market_release_date = models.DateField(verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    TYPE_CHOICES = [
        ('factory', 'Завод'),
        ('retail', 'Розничная сеть'),
        ('individual', 'Индивидуальный предприниматель'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип звена")
    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
        verbose_name="Поставщик"
    )

    debt = models.BigIntegerField(  # в поле IntegerField максимальное значение только 21 474 836.47р. может не хватить
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Задолженность (в копейках)"
    )
    currency = models.CharField(max_length=3, default='RUB', verbose_name="Валюта")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    products = models.ManyToManyField(Product, related_name='nodes', verbose_name="Продукты")

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self):
        return self.name

    @property
    def hierarchy_role(self):
        """Вычисляемая роль в иерархии: factory, distributor, retail."""
        if self.supplier is None:
            return "factory"
        # Проверяем, есть ли звенья, для которых текущее является поставщиком
        if self.customers.exists():
            return "distributor"
        return "retail"

    # def debt_in_rubles(self):
    #     """Вспомогательный метод для отображения задолженности в рублях (для админки и API)."""
    #     rubles = self.debt / 100.0
    #     return f"{rubles:.2f}".replace('.', ',')  # или просто число
