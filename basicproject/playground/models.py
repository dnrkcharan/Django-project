from django.db import models

# Manufacturers
class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=100)
    website = models.URLField()
    manufacturer_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.manufacturer_name

# Suppliers
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    country = models.CharField(max_length=100)
    website = models.URLField()
    supplier_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.supplier_name

# Products
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    manufacturers = models.ManyToManyField(Manufacturer, related_name="products_supplied", blank=True)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=100)
    release_date = models.DateField()
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, unique=True)
    images = models.ImageField(upload_to='product_images/')
    warranty_info = models.CharField(max_length=255)
    additional_specifications = models.TextField()
    suppliers = models.ManyToManyField(Supplier, related_name="products_supplied", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Indexing
    class Meta:
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
        ]

    

    def __str__(self):
        return self.product_name

# In this updated schema:

# The Supplier table has been added to represent suppliers, and it's related to both the Product and StockAvailability tables.
# The Product table now has a manufacturers field that allows multiple manufacturers to be associated with a product.
# The Product table also has a suppliers field that allows multiple suppliers to be associated with a product.
# The StockAvailability table includes a suppliers field to associate one or more suppliers with stock availability for a specific product.
# You can adapt this schema to your specific requirements and create a corresponding database diagram using a modeling tool.

# Store Locations
class StoreLocation(models.Model):
    store_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    manager_name = models.CharField(max_length=255)
    manager_contact = models.CharField(max_length=20)
    operating_hours = models.TextField()
    facilities = models.TextField()
    store_remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name

# Inventory
class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(StoreLocation, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    last_restock_date = models.DateTimeField()
    last_sold_date = models.DateTimeField()
    minimum_stock_threshold = models.PositiveIntegerField()
    maximum_stock_capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product} - {self.store}"

# Customers
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    billing_info = models.TextField()
    date_of_birth = models.DateField()
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    customer_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Indexing
    class Meta:
        indexes = [
            models.Index(fields=['customer_type']),
        ]

    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Orders
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    shipping_method = models.CharField(max_length=100)
    promo_code = models.CharField(max_length=100)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    payment_status = models.CharField(max_length=100)
    order_remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Indexing
    class Meta:
        indexes = [
            models.Index(fields=['status']),
        ]

    

    def __str__(self):
        return f"Order #{self.pk}"

# Order Details
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.product}"

# Payments
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    payment_remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order #{self.order_id}"

# Order Tracking
class OrderTracking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    tracking_date = models.DateTimeField()
    estimated_delivery_date = models.DateField()
    carrier_name = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)
    tracking_comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracking for Order #{self.order_id}"

# Invoices
class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_number = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    invoice_remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice for Order #{self.order_id}"
    
# Stock Availability
class StockAvailability(models.Model):
    store = models.ForeignKey(StoreLocation, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    reorder_threshold = models.PositiveIntegerField()
    reorder_quantity = models.PositiveIntegerField()
    suppliers = models.ManyToManyField(Supplier, related_name="available_products", blank=True)
    last_reorder_date = models.DateTimeField()
    remarks = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store} - {self.product}"

# Create your models here.
