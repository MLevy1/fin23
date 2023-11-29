from django.utils.text import slugify

def slugify_instance_payee(instance, save=False):
    slug = slugify(instance.payee)
    Klass = instance.__class__
    qs = Klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f"{slug}-{int(qs.count())+1}"
    instance.slug = slug
    if save:
        instance.save()