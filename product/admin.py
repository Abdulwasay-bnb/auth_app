from django.contrib import admin
from .models import  Products, Provider, Comments , CommentReply, Customer_Id, Cart,CartProduct
# Register your models here.


@admin.register(Products)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("title", "category", 'provider','created_by',"price")
    search_fields = ("title","price" )
    pass

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("company", "location", 'details')
    pass

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", 'product','comment')
    pass

@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "comment_p", 'reply')
    pass

@admin.register(Customer_Id)
class Customer_IdAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", 'phone_code','phone_number')
    pass

class CartProductInline(admin.TabularInline):  # You can also use StackedInline
    model = CartProduct
    extra = 1  # This ensures no extra blank forms are displayed by default
    classes = ('collapse', )
    fk_name = 'carts'  # Specify the foreign key to use
    def product_title(self, instance):
        return instance.product.title
    
    def product_provider_company(self,instance):
        return instance.product.provider.company

    def product_price(self, instance):
        return instance.product.price

    readonly_fields = ['product_title',  'product_provider_company', 'product_price']  # Make these fields read-only

    fields = ['product_title', 'product_provider_company', 'product_price']  # Specify the fields to display

    product_title.short_description = 'Product Title'  # Customizing column headers
    product_provider_company.short_desription = 'Provider'
    product_price.short_description = 'Product Price'
    

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", 'total_price')
    inlines = [CartProductInline]

@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = ("carts", "product")
    pass