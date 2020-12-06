from django.conf import settings
from django.contrib.auth.models import User as Profile
from django.db import models
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from HelloDjango.classes.choises import Section as Section
from django.db.models import F, Max, Min
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}

class Category(models.Model):
    code = models.CharField(max_length=50, null=False, unique=True,
                            verbose_name='Код')
    section = models.CharField(max_length=40, blank=True,
                               verbose_name='Секция')
    subsection = models.CharField(max_length=40, blank=True,
                               verbose_name='Подгруппа')
    name = models.CharField(max_length=100, null=False,
                            verbose_name='Наименование')
    slug = models.SlugField(unique=True, blank=True, max_length=100)
    producer = models.CharField(max_length=100, null=True, verbose_name='Производитель')
    flavor = models.CharField(max_length=100, null=True, verbose_name='Вкус')
    age = models.CharField(max_length=100, null=True, verbose_name='Возраст')
    description = models.TextField(null=True, blank=True,
                                   verbose_name='Описание')
    discount = models.IntegerField(verbose_name='Скидка', null=True, blank=True)
    maxPrice = models.FloatField(verbose_name='Максимальная цена', default=0)
    minPrice = models.FloatField(verbose_name='Минимальная цена', default=0)
    picture = models.ImageField(upload_to="static/images/categoryImage", null=True, blank=True,
                              verbose_name='Изображение')

    def save(self, *args, **kwargs):
        self.slug = slugify(''.join(alphabet.get(w, w) for w in self.name.lower()))
        super(Category, self).save(*args, **kwargs)
        
class Pricelist(models.Model):
    code = models.CharField(max_length=100, null=False, unique=True,
                            verbose_name='Код')
    category_id = models.ForeignKey(Category, related_name='pricelists', db_column='category_id', on_delete=models.PROTECT,
                              verbose_name='Группа')
    option = models.CharField(max_length=100, blank=True, null=True,
                              verbose_name='Опция')
    price = models.FloatField(verbose_name='Цена')
    count = models.IntegerField(verbose_name='Кол-во')
    discount = models.IntegerField(verbose_name='Скидка', null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Pricelist, self).save(*args, **kwargs)
        maxMin = Pricelist.objects.filter(category_id = self.category_id).aggregate(Max('price'), Min('price'))
        self.category_id.maxPrice = maxMin.get("price__max")
        self.category_id.minPrice = maxMin.get("price__min")
        self.category_id.save()
        

# class Post(models.Model):
#     author = models.CharField(max_length=200,
#                               verbose_name='Автор')
#     title = models.CharField(max_length=200,
#                              verbose_name='Заголовок')
#     text = models.TextField(verbose_name='Текст')
#     type = models.CharField(max_length=40, choices=Section.POST_CHOICES, default = "ARTICLE",
#                           verbose_name='Тип')
#     slug = models.SlugField(unique=True, blank=True)
#     picture = models.ImageField(upload_to="static/images/carousel_stocks", blank=True, null=True,
#                                 verbose_name='Изображение')
#     created_date = models.DateTimeField(default=timezone.now,
#                                         verbose_name='Дата создания')
#     published_date = models.DateTimeField(blank=True, null=True,
#                                           verbose_name='Дата публикации')
#     score = models.IntegerField(verbose_name='Просмотры', default = 0)

#     def __str__(self):
#         return self.title

#     def trunc_text(self):
#         return self.text[:150] + "..."

#     def save(self, *args, **kwargs):
#         self.slug = slugify(''.join(alphabet.get(w, w) for w in self.title.lower()))
#         super(Post, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name = _('Статья/Новость')
#         verbose_name_plural = _('Статьи и Новости')


# class Advertising(models.Model):
#     picture = models.ImageField(upload_to="static/images/carousel_stocks", blank=True, default='',
#                                 verbose_name='Изображение')
#     text = models.TextField(verbose_name='Текст')
#     link = models.URLField(verbose_name='Ссылка')
#     date_start = models.DateTimeField(default=timezone.now,
#                                       verbose_name='Дата начала')
#     date_end = models.DateTimeField(blank=True, null=True,
#                                     verbose_name='Дата окончания')
#     active = models.BooleanField(verbose_name='Активно')

#     def __str__(self):
#         return self.text

#     def photo_pic(self):
#         return format_html(
#             "<div class='photo_pic'><div style='background-image: url(/media/{})'></div></div>",
#             self.picture,
#         )

#     class Meta:
#         verbose_name = _('Реклама')
#         verbose_name_plural = _('Реклама')


# class Request(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True,
#                              verbose_name='Пользователь')
#     name = models.CharField(max_length=50, blank=True, null=True,
#                             verbose_name='Имя')
#     phone = models.CharField(max_length=12, blank=True, null=True,
#                              verbose_name='Телефон')
#     add_date = models.DateTimeField(blank=True, null=True,default=timezone.now,
#                                     verbose_name='Дата создания')
#     goods = models.ManyToManyField(Pricelist, verbose_name='Товар', through='PriceRequest')

#     state = models.CharField(max_length=10, choices=Section.STATE_CHOICES, default='INACTIVE',
#                              verbose_name='Статус')
#     info = models.TextField(blank=True, null=True,
#                             verbose_name='Дополнительная информация')
#     email = models.EmailField(verbose_name='Email',blank=True, null=True)

#     discount = models.IntegerField(verbose_name='Общая скидка',blank=True, null=True)
    
#     def __str__(self):
#         return "Заявка"
#         # if self.user:
#         #     return self.user.user.username()
#         # else:
#         #     return self.name

#     def get_goods(self):
#         return "\n".join([p.name for p in self.goods.all()])
        
#     def summ(self):
#         summ_raw = 0
#         summ_finish = 0
        
#         for p in self.goods.all():
            
#             good = PriceRequest.objects.get(req=self.id, pricel=p.id)
#             count = good.count
#             price = good.price
            
#             summ_raw += count*p.price;
#             summ_finish=summ_finish + count*price 
#             # if p.group.discount:
#             #   summ_finish=summ_finish + count*price  * (1 - p.group.discount/100)
#             # elif p.discount:
#             #     summ_finish=summ_finish + count*price * (1 - p.discount/100)
#             # else:
#             #     summ_finish += count*price
#         if self.discount:
#             summ_finish = summ_finish*(1 - self.discount/100)
#         return {"summ_raw": summ_raw, "summ_finish": summ_finish}

#     class Meta:
#         verbose_name = _('Заявка')
#         verbose_name_plural = _('Заявки')
        
#     def save(self, *args, **kwargs):
#         if self.id is None:
#             em = self.__dict__
#             if self.user_id:
#                 profile = Profile.objects.get(id=self.user_id)
#                 self.email = profile.user.email
#                 self.phone = profile.phone
#                 self.name = profile.user.first_name
#         super(Request, self).save(*args, **kwargs)    
        
        
# class PriceRequest(models.Model):
#     req = models.ForeignKey(Request, related_name="request_req",
#                     on_delete=models.CASCADE, verbose_name='Заявка')
#     pricel = models.ForeignKey(Pricelist, related_name="pricelist_price",
#             on_delete=models.CASCADE, verbose_name='Товар')
#     price = models.FloatField(verbose_name='Цена', default=0)
#     count = models.IntegerField(verbose_name='Количество', default=1)
    
#     def save(self, *args, **kwargs):
#         if self.id is None:
#             pr_req = PriceRequest.objects.filter(pricel_id=self.pricel_id, req_id=self.req_id)
            
#             if len(pr_req) > 0:
                
#                 pr_req.update(count = F('count')+self.count)
#                 return
#             else:
#                 pricel = Pricelist.objects.get(id=self.pricel_id)
#                 if pricel.group.discount:
#                     self.price = pricel.price * (1 - pricel.group.discount/100)
#                 elif pricel.discount:
#                     self.price = pricel.price * (1 - pricel.discount/100)
#                 else:
#                     self.price = pricel.price;    
#         super(PriceRequest, self).save(*args, **kwargs)
        
        

# @receiver(post_delete, sender=Pricelist)
# def auto_delete_photo_on_delete(sender, instance, **kwargs):
#     if instance.photo:
#         if os.path.isfile(instance.photo.path):
#             os.remove(instance.photo.path)
            
# @receiver(pre_save, sender=Pricelist)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return False

#     try:
#         old_file = Pricelist.objects.get(pk=instance.pk).photo
#     except MediaFile.DoesNotExist:
#         return False

#     new_file = instance.photo
#     if old_file and old_file != new_file:
#         if os.path.isfile(old_file.path):
#             os.remove(old_file.path)
            
@receiver(post_delete, sender=Category)            
# @receiver(post_delete, sender=PricelistElementImage)     
# @receiver(post_delete, sender=Advertising)
def auto_delete_picture_on_delete(sender, instance, **kwargs):
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)
            

@receiver(pre_save, sender=Category)            
# @receiver(pre_save, sender=PricelistElementImage)     
# @receiver(pre_save, sender=Advertising)
def auto_delete_picture_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = sender.objects.get(pk=instance.pk).picture
    except MediaFile.DoesNotExist:
        return False

    new_file = instance.picture
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)            

