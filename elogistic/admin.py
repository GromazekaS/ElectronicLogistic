from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django import forms
from .models import NetworkNode, Product


class NetworkNodeForm(forms.ModelForm):
    """
    Форма для NetworkNode, преобразующая рубли в копейки и обратно.
    """
    debt_rub = forms.DecimalField(
        max_digits=12, decimal_places=2,
        label='Задолженность (руб)',
        required=False,
        help_text='Введите сумму в рублях (копейки через точку)'
    )
    debt_display = forms.CharField(
        label='Текущая задолженность',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'style': 'background:#f0f0f0;'})
    )

    class Meta:
        model = NetworkNode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            rubles = self.instance.debt / 100.0
            # Форматируем с разделителями тысяч и знаком рубля
            formatted = f"{rubles:,.2f}".replace(',', ' ') + " ₽"
            self.fields['debt_display'].initial = formatted
            self.fields['debt_rub'].initial = rubles
        else:
            self.fields['debt_display'].initial = '0.00 ₽'
            self.fields['debt_rub'].initial = 0

    def save(self, commit=True):
        rub = self.cleaned_data.get('debt_rub')
        if rub is not None:
            self.instance.debt = int(rub * 100)
        return super().save(commit)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    form = NetworkNodeForm
    list_display = ('name', 'city', 'hierarchy_role', 'supplier_link', 'debt_display', 'created_at')
    list_filter = ('city',)
    search_fields = ('name', 'city')
    actions = ['clear_debt']
    readonly_fields = ('created_at',)  # created_at не редактируется
    filter_horizontal = ('products',)

    fieldsets = (
        (None, {
            'fields': ('type', 'name', 'email', ('country', 'city'), ('street', 'house_number'))
        }),
        ('Связи', {
            'fields': ('supplier', 'products')
        }),
        ('Финансы', {
            'fields': ('debt_display', 'debt_rub', 'currency')
        }),
        ('Дата создания', {
            'fields': ('created_at',)
        }),
    )

    def supplier_link(self, obj):
        """Возвращает HTML-ссылку на страницу поставщика."""
        if obj.supplier:
            url = reverse('admin:elogistic_networknode_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"
    supplier_link.short_description = "Поставщик"
    supplier_link.admin_order_field = 'supplier__name'  # позволяет сортировать по имени поставщика

    def debt_display(self, obj):
        """Отображает задолженность в рублях."""
        return f"{obj.debt / 100:.2f} ₽"
    debt_display.short_description = "Задолженность"
    debt_display.admin_order_field = 'debt'

    def clear_debt(self, request, queryset):
        """Action для очистки задолженности."""
        queryset.update(debt=0)
        self.message_user(request, "Задолженность очищена у выбранных звеньев.")
    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    def get_queryset(self, request):
        """Оптимизация запросов: подгружаем supplier и customers для вычисления hierarchy_role."""
        return super().get_queryset(request).select_related('supplier').prefetch_related('customers')

    def debt_display(self, obj):
        rubles = obj.debt / 100.0
        # Форматируем с разделителями тысяч (запятая) и заменяем запятую на пробел
        formatted = f"{rubles:,.2f}".replace(',', ' ') + " ₽"
        return formatted
    debt_display.short_description = "Задолженность"
    debt_display.admin_order_field = 'debt'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'market_release_date')
    search_fields = ('name', 'model')
