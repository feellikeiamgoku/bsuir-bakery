from django.db import models
from datetime import date, datetime
from authenication.models import User

class OrderStatuses(models.TextChoices):
    WAITING = "Ждет обработку", "Ждет обработку"
    COOKING = ("Готовится", "Готовится")
    READY =  ("Готов", "Готов")
    COMPLETED = ("Выполнен", "Выполнен")
    REFUSED = ("Отменён", "Отменён")

    @property
    def user_statuses(self):
        return [self.WAITING, self.REFUSED]

class PaymentMethods(models.TextChoices):
    CASH = "Наличными", "Наличными"
    CARD = "Картой", "Картой"

class Product(models.Model):
    name = models.CharField(verbose_name="Название продукта", max_length=100)
    description = models.TextField(verbose_name="Описание", null=True)
    price = models.FloatField(verbose_name="Цена")
    weight = models.PositiveIntegerField(verbose_name="Вес")
    time_to_cook = models.PositiveIntegerField("Время готовки в минутах")
    image = models.ImageField("Изображение", upload_to="products", null=True)

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=20)
    products = models.ManyToManyField(Product, "category", blank=True)

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    
    def __str__(self):
        return f"{self.product_id} в кол-ве {self.quantity}"



class Case(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="case")
    products = models.ManyToManyField(OrderProduct, related_name="case", blank=True)


    def get_total_price(self):
        total = self.products.all().aggregate(total=models.Sum(models.F("product_id__price") * models.F("quantity")))
        return total["total"]
    
    def get_total_products(self):
        total = self.products.aggregate(total=models.Sum("quantity"))
        return total["total"]

    def __str__(self):
        return f"Корзина пользователя № {self.user.id}"


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(OrderProduct, related_name="order")
    status = models.CharField(choices=OrderStatuses.choices, max_length=20, default=OrderStatuses.WAITING, verbose_name="Статус заказа")
    payment_method = models.CharField(choices=PaymentMethods.choices, max_length=20, verbose_name="Способ оплаты")
    created = models.DateTimeField(verbose_name="Дата создания", default=datetime.now, blank=True)
    updated = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        total = self.products.all().aggregate(total=models.Sum(models.F("product_id__price") * models.F("quantity")))
        return total["total"]
    
    def get_total_products(self):
        total = self.products.aggregate(total=models.Sum("quantity"))
        return total["total"]


    def __str__(self) -> str:
        return f"Заказ для пользователя № {self.user_id.id}"


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    time_created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    text = models.TextField(verbose_name="Текст отзыва")
    raitng = models.PositiveSmallIntegerField("Рейтинг", blank=True)

    def __str__(self) -> str:
        return f"Отзыв пользователя № {self.author.id}"


class ProductReview(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    time_created = models.DateTimeField(verbose_name="Дата создания", auto_now=True)
    text = models.TextField(verbose_name="Текст отзыва")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт", related_name="reviews")

    def __str__(self) -> str:
        return f"Отзыв пользователя № {self.author.id}"