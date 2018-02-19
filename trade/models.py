from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


def upload_profile_image(instance, filename):
    user = User.objects.get(id=instance.id)
    return '{}/{}/{}'.format("Users", user.id, 'profile_image.jpg')


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        ('superuser'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as super user or not . '
            'Unselect this instead of deleting accounts.'
        ),
    )

    has_perm = models.BooleanField(
        ('perm'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as super user or not . '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def has_perm(self, arg):
        if self.is_superuser:
            return True
        return False

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return str(self.id)


def upload_product_image(instance, filename):
    now_time = datetime.now().microsecond
    return '{}/{}'.format("Products", '%s.jpg' % now_time)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return str(self.id)


class Product(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.CharField(max_length=200)
    size = models.CharField(max_length=50)
    dimensions = models.CharField(max_length=50)
    price = models.FloatField(default=0.0)
    manufacturer = models.CharField(max_length=50)
    image = models.ImageField(upload_to=upload_product_image, null=True, blank=True)
    stock = models.IntegerField(default=0)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class ProductImage(models.Model):
    image = models.ImageField(upload_to=upload_product_image, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class ProductPurchased(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "ProductPurchased"

    def __str__(self):
        return str(self.id)


class PromoCode(models.Model):
    title = models.CharField(max_length=100)
    discount_percent = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    INPROGRESS = 'inprogress'
    PROCESSED = 'processed'

    STATUS_TYPE = (
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
        (INPROGRESS, 'In Progress'),
        (PROCESSED, 'Processed')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased_product = models.ManyToManyField(ProductPurchased)
    promocode = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_TYPE, default=INPROGRESS)
    address = models.CharField(max_length=200)
    cost = models.FloatField(default=0.0)
    time = models.DateTimeField()

    def __str__(self):
        return str(self.id)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    CASH = 'cash'
    CARD = 'card'

    PAYMENT_TYPE = (
        (CASH, 'Cash On Delivery'),
        (CARD, 'Card')
    )

    amount = models.FloatField(default=0.0)
    date = models.DateTimeField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE, default=CARD)

    def __str__(self):
        return str(self.id)



class WishList(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Shipment(models.Model):
    pass
