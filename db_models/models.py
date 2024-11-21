from django.db import models
import os

from django.forms import ImageField


class Banners(models.Model):
    """
        banner modelida saytni yuqoriq qismdagi rasm va rangni qo'shish o'zgartirish va o'chirish imkoniyatini
        yaratib beradi
    """
    title = models.CharField(max_length=50, verbose_name='title')
    head_color = models.CharField(max_length=20)
    footer_color = models.CharField(max_length=20)
    image = models.ImageField(upload_to="banners/", unique=True, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'banners'
        indexes = [
            models.Index(fields=['id'])
        ]

    def delete(self, *args, **kwargs):
        # model o'chirilishidan oldin faylni o'chirish
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)


class MenuElements(models.Model):
    """
    menu elementlari saqlanadigan model bunda biror sahifaga o'tganda
     sahifa nomi va o'sha sahifani yuqori qismi rangi va qanaqadir
      rasm qo'yilmoqchi bo'lsa rasm qo'yish mumkin
    """
    name_ru = models.CharField(max_length=50)
    link_ru = models.CharField(max_length=50)
    name_uz = models.CharField(max_length=50)
    link_uz = models.CharField(max_length=50)
    status = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'menu_elements'
        indexes = [
            models.Index(fields=['id'])
        ]


class Menu(models.Model):
    """
    menu elementlari saqlanadigan model bunda hamma
    yaratilgan menu elementlarini bir joyda saqlash imkonini beradi
    """
    name = models.CharField(max_length=50)
    shortcut = models.CharField(max_length=50)
    language = models.CharField(max_length=50)
    menu_elements = models.ManyToManyField(MenuElements, blank=True)
    banner = models.ForeignKey(Banners, on_delete=models.CASCADE, null=False)
    status = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'menu'
        indexes = [
            models.Index(fields=['id'])
        ]


class StatisticItems(models.Model):
    """
     statistic elementlari saqlanadigan jadval
      qandaydir baxolash mezoni qo'shish mumkin
    """
    title_ru = models.CharField(max_length=50)
    title_uz = models.CharField(max_length=50)
    order_count = models.IntegerField()
    number_responses = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'statistic_items'
        indexes = [
            models.Index(fields=['id'])
        ]


class Statistics(models.Model):
    """ statistika sarlavhasi saqlanadigan model
    bu modelga sarlavha qo'yib statistic_items jadvalidagi ma'lumotlarni qo'shimiz mukin"""

    title_ru = models.CharField(max_length=50)
    title_uz = models.CharField(max_length=50)
    statistic_items = models.ManyToManyField(StatisticItems, blank=True)
    status = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'statistics'
        indexes = [
            models.Index(fields=['id'])
        ]


class TegRegions(models.Model):
    """ filiali bor viloyatlar ro'yhati uchun kamchilik bo'lishi mukin"""
    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    sorting = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'teg_regions'
        indexes = [
            models.Index(fields=['id'])
        ]


class TegWorkingDays(models.Model):
    """ ish kunlarini saqlash uchun kerak bo'lgan jadval"""
    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    sorting = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'teg_working_days'
        indexes = [
            models.Index(fields=['id'])
        ]


class TegExperience(models.Model):

    """ ish tajribasi ro'yhati jadvali kamchilik bo'lishi mukin"""

    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    sorting = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'teg_experience'
        indexes = [
            models.Index(fields=['id'])
        ]


class TegVacancies(models.Model):

    """ vacansiya uchun teglar ro'yhati jadvali'"""

    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    sorting = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'teg_vacancies'
        indexes = [
            models.Index(fields=['id'])
        ]


class TegBranches2(models.Model):

    """ filiallar uchun teglar ro'yhati jadvali 2 """

    name_ru = models.CharField(max_length=100)
    name_uz = models.CharField(max_length=100)
    sorting = models.IntegerField(default=1)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'teg_branches'
        indexes = [
            models.Index(fields=['id'])
        ]


class Vacancies(models.Model):

    """
    vacansiyalar ro'yhati jadvali'
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    teg_vacancies = models.ManyToManyField(TegVacancies, blank=True)
    shablon = models.CharField(max_length=50)
    teg_regions = models.ManyToManyField(TegRegions, blank=True)
    teg_experiences = models.ManyToManyField(TegExperience, blank=True)
    price_ru = models.CharField(max_length=100, null=True, blank=True)
    price_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'vacancies'
        indexes = [
            models.Index(fields=['id'])
        ]


class Purchases(models.Model):
    """
     bu model xaridlar jadvali hisoblanadi
        yani закупки
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'purchases'
        indexes = [
            models.Index(fields=['id'])
        ]


class Marks(models.Model):
    """
     bu model markalar modeli hisoblanadi jadvali hisoblanadi
        yani закупки
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    marks_count_ru = models.CharField(max_length=100, null=True, blank=True)
    marks_count_uz = models.CharField(max_length=100, null=True, blank=True)
    years = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'marks'
        indexes = [
            models.Index(fields=['id'])
        ]


class SaveMediaFiles(models.Model):
    """
        umumiy mediya yoki pdf filelarni saqlash uchun yaratilgan model
    """
    file = models.FileField(upload_to='')
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('id', )
        db_table = 'save_media_files'
        indexes = [
            models.Index(fields=['id'])
        ]


class Events(models.Model):
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    video_preview = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='video_preview_events')
    video = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='video_events')
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    teg_branches = models.ManyToManyField(TegBranches2, blank=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'events'
        indexes = [
            models.Index(fields=['id'])
        ]


class UzPostNews(models.Model):
    """yangiliklar jadvaliga o'zbekcha ruscha ma'lumotlar saqlanadi"""
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    image_caption_ru = models.CharField(max_length=100, null=True, blank=True)
    image_caption_uz = models.CharField(max_length=100, null=True, blank=True)
    image_ru = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='image_ru_uzpostnews')
    image_uz = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='image_uz_uzpostnews')
    video_preview_ru = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='video_preview_ru_uzpostnews')
    video_preview_uz = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='video_preview_uz_uzpostnews')
    video_ru = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='video_ru_uzpostnews')
    video_uz = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='video_uz_uzpostnews')
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'uz_post_news'
        indexes = [
            models.Index(fields=['id'])
        ]


class PostalServices(models.Model):
    """
     pochta usluga jadvali bundan ruscha uzbekcha ma'lumotlar saqlanadi
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'postal_services'
        indexes = [
            models.Index(fields=['id'])
        ]


class Pages(models.Model):
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'pages'
        indexes = [
            models.Index(fields=['id'])
        ]


class CategoryPages(models.Model):
    """ Category pages bu model uzpostda tariflar sahifasi uchun tariflar categoriyasi kerak"""
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    pages = models.ManyToManyField(Pages, blank=True, related_name='category_pages')

    class Meta:
        ordering = ('id',)
        db_table = 'category_page'
        indexes = [
            models.Index(fields=['id'])
        ]


class ControlCategoryPages(models.Model):
    """ Control category pages bu model uzpostda category lar uchun2-category vazifasini bajaradi"""
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    page_categories = models.ManyToManyField(CategoryPages, blank=True, related_name='control_categories')

    class Meta:
        ordering = ('id', )
        db_table = 'control_categories'
        indexes = [
            models.Index(fields=['id'])
        ]


class BranchServices(models.Model):
    """
        branch services model filial xizmat ko'rsatish jadvali
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'branch_services'
        indexes = [
            models.Index(fields=['id'])
        ]


class ShablonServices(models.Model):
    """
    filiallar ro'yhati uchun kerak bo'lgan usluga yaratish jadvali
    """

    title_ru = models.CharField(max_length=50, null=True, blank=True)
    title_uz = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('id', )
        db_table = 'shablon_servises'
        indexes = [
            models.Index(fields=['id'])
        ]


class Branches(models.Model):
    """ filiallar ro'yhati saqlanadigan jadval"""
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    shortcut_ru = models.SlugField(max_length=100, unique=True)
    shortcut_uz = models.SlugField(max_length=100, unique=True)
    meta_title_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_title_uz = models.CharField(max_length=100, null=True, blank=True)
    meta_description_ru = models.TextField(null=True, blank=True)
    meta_description_uz = models.TextField(null=True, blank=True)
    meta_words_ru = models.CharField(max_length=100, null=True, blank=True)
    meta_words_uz = models.CharField(max_length=100, null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    facts = models.CharField(max_length=100, null=True, blank=True)
    address_ru = models.CharField(max_length=100, null=True, blank=True)
    address_uz = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    deputy_director = models.CharField(max_length=100, null=True, blank=True)
    work_time = models.CharField(max_length=100, null=True, blank=True)
    header_image = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='header_image')
    branch_sidebar_image = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='branches_sidebar_image')
    postal_service = models.ManyToManyField(ShablonServices, blank=True, related_name='postal_service')
    kurier_services = models.ManyToManyField(ShablonServices, blank=True, related_name='kurier_services')
    additional_services = models.ManyToManyField(ShablonServices, blank=True, related_name='additional_services')
    contractual_services = models.ManyToManyField(ShablonServices, blank=True, related_name='contractual_services')
    modern_ict_services = models.ManyToManyField(ShablonServices, blank=True, related_name='modern_ict_services')
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    working_days = models.ManyToManyField(TegWorkingDays, blank=True)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'branches'
        indexes = [
            models.Index(fields=['id'])
        ]


class VacanciesImages(models.Model):
    """
    vacansiyalar ro'yhati uchun head qismida chiqib turadigan rasmlar
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'vacancies_images'
        indexes = [
            models.Index(fields=['id'])
        ]


class InternalDocuments(models.Model):
    """
    Internal Documents jadvali document ma'lumotlarini saqlaydigan jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'internal_documents'
        indexes = [
            models.Index(fields=['id'])
        ]


class ThemaQuestions(models.Model):
    """
    tema voprosi jadvali malumotlarni saqlaydi
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id', )
        db_table = 'thema_questions'
        indexes = [
            models.Index(fields=['id'])
        ]


class BusinessPlansCompleted(models.Model):
    """
        Бизнес-план «Виполнение» jadvali yuqoridagi theme_questions jadvali bilan bir xil malumot yuklanadi
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'business_plans_completed'
        indexes = [
            models.Index(fields=['id'])
        ]


class AnnualReports(models.Model):
    """
        yullik hisobotlar saqlanadigan jadval
    """

    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'annual_reposts'
        indexes = [
            models.Index(fields=['id'])
        ]


class Dividends(models.Model):
    """
       ruschasiga дивиденды deb nomlangan jadval dividentlarni saqlovchi jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'dividends'
        indexes = [
            models.Index(fields=['id'])
        ]


class QuarterReports(models.Model):
    """ chorak hisobotlarni saqlovchi jadval"""
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'quarter_reports'
        indexes = [
            models.Index(fields=['id'])
        ]


class UserInstructions(models.Model):
    """
    foydalanuvchi ko'rsatmalar ro'yhagti
    (инструкции пользователя)
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'user_instructions'
        indexes = [
            models.Index(fields=['id'])
        ]


class ExecutiveApparatus(models.Model):
    """
        ijro apparati yani ijro bo'lim boshliqlari ro'yhati
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    branch_ru = models.CharField(max_length=100, null=True, blank=True)
    branch_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'executive_apparatus'
        indexes = [
            models.Index(fields=['id'])
        ]


class ShablonUzPostTelNumber(models.Model):
    """
    contact jadvali uchun shablon uzpost telnummer
    jadvali
    """
    tel_number = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('id',)
        db_table = 'shablon_uzpost_tel_number'
        indexes = [
            models.Index(fields=['id'])
        ]


class ShablonContactSpecialTitle(models.Model):
    """
    contact modeli uchun many to many bo'g'laandigan shablon
    """
    title_ru = models.CharField(max_length=100, null=True, blank=True)
    title_uz = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('id',)
        db_table = 'shablon_contact_special_title'
        indexes = [
            models.Index(fields=['id'])
        ]


class Contact(models.Model):
    """
    contact modeli uzpost haqida ma'lumotlar
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    tel_number = models.ManyToManyField(ShablonUzPostTelNumber, blank=True)
    title_2 = models.ManyToManyField(ShablonContactSpecialTitle, blank=True, related_name='title_2')
    description_2 = models.ManyToManyField(ShablonContactSpecialTitle, blank=True, related_name='description_2')
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'contact'
        indexes = [
            models.Index(fields=['id'])
        ]


class Advertisements(models.Model):
    """
    reklamalar jadvali

    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'advertisements'
        indexes = [
            models.Index(fields=['id'])
        ]


class OrganicManagements(models.Model):
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    tel_number = models.CharField(max_length=50, null=True, blank=True)
    facts = models.CharField(max_length=50, null=True, blank=True)
    working_time = models.CharField(max_length=50, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    working_days = models.ManyToManyField(TegWorkingDays, blank=True, related_name='working_days')
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'organic_managements'
        indexes = [
            models.Index(fields=['id'])
        ]


class Partners(models.Model):
    """
        hamkorlar jadvali malumotlarini saqlash uchun model
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    image_ru = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='image_ru')
    image_uz = models.ManyToManyField(SaveMediaFiles, blank=True, related_name='image_uz')
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'partners'
        indexes = [
            models.Index(fields=['id'])
        ]


class RegionalBranches(models.Model):
    """
    Regional Branches jadvali viloyat filiallari ma'lumotlari saqlanadigan jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    filial_name_ru = models.CharField(max_length=100, null=True, blank=True)
    filial_name_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'regional_branches'
        indexes = [
            models.Index(fields=['id'])
        ]


class Advertising(models.Model):
    """
        Reklamalarni yaratish saqlash jadvali
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'advertising'
        indexes = [
            models.Index(fields=['id'])
        ]


class InformationAboutIssuer(models.Model):
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'information_about_issuer'
        indexes = [
            models.Index(fields=['id'])
        ]


class Slides(models.Model):
    """
    slidelar jadvali asosan bosh menuga chiqariladigan ma'lumotlarni saqlaydi
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    google_play = models.CharField(max_length=100, null=True, blank=True)
    app_store = models.CharField(max_length=100, null=True, blank=True)
    knopka_1_ru = models.CharField(max_length=100, null=True, blank=True)
    link_1_ru = models.CharField(max_length=100, null=True, blank=True)
    knopka_1_uz = models.CharField(max_length=100, null=True, blank=True)
    link_1_uz = models.CharField(max_length=100, null=True, blank=True)
    knopka_2_ru = models.CharField(max_length=100, null=True, blank=True)
    link_2_ru = models.CharField(max_length=100, null=True, blank=True)
    knopka_2_uz = models.CharField(max_length=100, null=True, blank=True)
    link_2_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'slides'
        indexes = [
            models.Index(fields=['id'])
        ]


class SocialMedia(models.Model):
    """
    ijtimoiy tarmoqlardagi faol profillarni saqlaydiagn jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'social_medial'
        indexes = [
            models.Index(fields=['id'])
        ]


class EssentialFacts(models.Model):
    """
        muhim bo'lgan factlarni saqlash uchun kerak bo'lgan jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'essential_facts'
        indexes = [
            models.Index(fields=['id'])
        ]


class Rates(models.Model):
    """
     tariflarni saqlaydigan jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'rates'
        indexes = [
            models.Index(fields=['id'])
        ]


class Services(models.Model):

    """
    xizmatlar malumotlarini saqlanadigan jadval
    """

    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'services'
        indexes = [
            models.Index(fields=['id'])
        ]

##################################################################### new


class CategoryServices(models.Model):
    name_uz = models.CharField(max_length=200, null=True, blank=True)
    name_ru = models.CharField(max_length=200, null=True, blank=True)
    services_id = models.ManyToManyField(Services, related_name='category_services', blank=True)

    class Meta:
        ordering = ('id',)
        db_table = 'category_services'
        indexes = [
            models.Index(fields=['id'])
        ]
###########################################################################


class CharterSociety(models.Model):
    """
    ustav jamiyat ma'lumotlarini saqlaydigan jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'charter_society'
        indexes = [
            models.Index(fields=['id'])
        ]


class SecurityPapers(models.Model):
    """
    xavfsizlik hujjatlari saqlanadigan jadval
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'security_papers'
        indexes = [
            models.Index(fields=['id'])
        ]


class FAQ(models.Model):
    """
    ko'p so'raladigan savollar jadvali malumotlarni saqlash uchun model ORM dan foydalangan holda
    """
    title_ru = models.CharField(max_length=100)
    title_uz = models.CharField(max_length=100)
    description_ru = models.TextField(null=True, blank=True)
    description_uz = models.TextField(null=True, blank=True)
    text_ru = models.TextField(null=True, blank=True)
    text_uz = models.TextField(null=True, blank=True)
    link_ru = models.CharField(max_length=100, null=True, blank=True)
    link_uz = models.CharField(max_length=100, null=True, blank=True)
    tel_number = models.CharField(max_length=100, null=True, blank=True)
    name_knopka_ru = models.CharField(max_length=100, null=True, blank=True)
    name_knopka_uz = models.CharField(max_length=100, null=True, blank=True)
    link_knopka_ru = models.CharField(max_length=100, null=True, blank=True)
    link_knopka_uz = models.CharField(max_length=100, null=True, blank=True)
    title_2_ru = models.CharField(max_length=100, null=True, blank=True)
    title_2_uz = models.CharField(max_length=100, null=True, blank=True)
    description_2_ru = models.TextField(null=True, blank=True)
    description_2_uz = models.TextField(null=True, blank=True)
    save_image = models.ImageField(upload_to='images/', null=True, blank=True)
    shablon = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_created=True)

    class Meta:
        ordering = ('id',)
        db_table = 'faq'
        indexes = [
            models.Index(fields=['id'])
        ]


class SiteSettings(models.Model):
    """
    bunda sitega tegishli bo'lgan komandalar yoziladi
    """
    name = models.CharField(max_length=100)
    tab = models.CharField(max_length=100, null=False)
    ru = models.CharField(max_length=150, null=False)
    uz = models.CharField(max_length=150, null=False)
    eng = models.CharField(max_length=150, null=False)

    class Meta:
        ordering = ('id', )
        db_table = 'site_settings'
        indexes = [
            models.Index(fields=['id'])
        ]
