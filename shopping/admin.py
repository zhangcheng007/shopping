from django.contrib import admin
from models import Character,Contact,Tag,Category,Product,ProductPic,ProductSpec

# Register your models here.
class TagInline(admin.TabularInline):
    model = Tag


class ContactAdmin(admin.ModelAdmin):
     inlines = [TagInline]
     fieldsets = (
        ['Main',{
            'fields':('name','email'),
        }],
        ['Advance',{
            'classes': ('collapse',), # CSS
            'fields': ('age',),
        }]
     )
     search_fields = ('name',)



#admin.site.register(Contact,ContactAdmin)

#admin.site.register([Character])


class ProductPicInline(admin.TabularInline):
    model =ProductPic
    extra = 1



class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'pic', 'parent','created_on','is_active')
    #inlines = [ProductInline]

admin.site.register(Category,CategoryAdmin)



class ProductPicInline(admin.TabularInline):
    model =ProductPic
    extra = 1

class ProductSpecInline(admin.TabularInline):
    model =ProductSpec
    extra = 1



class ProductAdmin(admin.ModelAdmin):
     search_fields = ['name']
     list_display = ('name', 'category', 'price','quantity','created_on')
     inlines = [ProductPicInline,ProductSpecInline]

admin.site.register(Product,ProductAdmin)









