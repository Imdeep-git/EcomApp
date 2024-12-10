from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save

# SubCategory Model
class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)

    def __str__(self):
        return self.subcategory_name


# Category Model
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    category_icon = models.ImageField(upload_to='categories/icons/')
    category_image = models.ImageField(upload_to='categories/images/')
    subcategories = models.ManyToManyField(SubCategory, related_name='categories')

    def __str__(self):
        return self.category_name


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    stock_quantity = models.IntegerField()
    specifications = models.JSONField(default='', help_text="Store product specifications as a dictionary (e.g., {'processor': 'Intel i7', 'ram': '16GB'}). You can add any key-value pairs relevant to the product.")
    slug = models.SlugField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


# Function to create a unique slug for the product
def create_slug(instance):
    slug = slugify(instance.name)
    
    if instance.pk: 
        similar_slugs = Product.objects.filter(slug__startswith=slug).exclude(pk=instance.pk)
        if similar_slugs.exists():
            slug = f"{slug}-{similar_slugs.count() + 1}"
    else:
        #For new instance, just crete the slug
        similar_slugs = Product.objects.filter(slug=slug)
        if similar_slugs.exists():
            slug = f"{slug}-{similar_slugs.count() + 1}"

    return slug


# Signal to create a slug before saving the product
def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:  #generates slug if it doesn't exist
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_product_receiver, sender=Product)


# Productimage Model
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"Image for {self.product.name}"
