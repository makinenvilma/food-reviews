from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = BlogPage.objects.child_of(self).live()

        selected_location = request.GET.get('location', '')
        selected_min_rating = request.GET.get('rating', '')

        if selected_location:
            blogpages = blogpages.filter(location=selected_location)
        if selected_min_rating.isdigit():
            blogpages = blogpages.filter(rating__gte=int(selected_min_rating))

        all_locations = (
            BlogPage.objects.child_of(self).live()
            .exclude(location='')
            .values_list('location', flat=True)
            .distinct()
            .order_by('location')
        )

        context['blogpages'] = blogpages.order_by('-first_published_at')
        context['available_locations'] = all_locations
        context['selected_location'] = selected_location
        context['selected_min_rating'] = selected_min_rating
        return context
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogPage(Page):
    date = models.DateField("Post date")
    restaurant_name = models.CharField(max_length=120, blank=True)
    location = models.CharField(max_length=120, blank=True, default="Helsinki, Finland")
    product = models.CharField(max_length=160, blank=True)
    price = models.CharField(max_length=40, blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, f"{i} tahtea") for i in range(1, 6)],
        default=5,
    )
    taste = RichTextField(blank=True)
    sides = RichTextField(blank=True)
    service = RichTextField(blank=True)
    overall = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('taste'),
        index.SearchField('sides'),
        index.SearchField('service'),
        index.SearchField('overall'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('restaurant_name'),
            FieldPanel('location'),
            FieldPanel('product'),
            FieldPanel('price'),
            FieldPanel('rating'),
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Arvostelun tiedot"),
        MultiFieldPanel([
            FieldPanel('taste'),
            FieldPanel('sides'),
            FieldPanel('service'),
            FieldPanel('overall'),
        ], heading="Arvostelun osiot"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    @property
    def stars(self):
        return [i < self.rating for i in range(5)]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'

class BlogTagIndexPage(Page):

    def get_context(self, request):

        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context