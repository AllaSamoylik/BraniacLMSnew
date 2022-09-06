from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

NULLABLE = {'blank': True, 'null': True}


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Edited", editable=False)
    deleted = models.BooleanField(default=False, verbose_name="Deleted")

    class Meta:
        abstract = True
        ordering = ('-created',)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    def live(self):
        self.deleted = False
        self.save()

    def hard_delete(self):
        super(BaseModel, self).delete()


class BaseQuerySet(QuerySet):

    def delete(self, *args, **kwargs):
        return super(BaseQuerySet, self).update(deleted=True)

    def hard_delete(self):
        return super(BaseQuerySet, self).delete()


class NewsManager(models.Manager):

    def get_queryset(self):
        return BaseQuerySet(self.model).filter(deleted=False)


class CoursesManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model).filter(deleted=False)


class News(BaseModel):

    objects = NewsManager()
    all_objects = models.Manager()

    title = models.CharField(max_length=256, verbose_name="Title")
    preamble = models.CharField(max_length=1024, verbose_name="Preamble")
    body = models.TextField(verbose_name="Body", **NULLABLE)
    body_as_markdown = models.BooleanField(default=False, verbose_name="As markdown")

    def __str__(self) -> str:
        return f"{self.pk} {self.title}"

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = ('-created',)


class Course(BaseModel):
    objects = CoursesManager()
    all_objects = models.Manager()

    name = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Cost", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Cover")

    def __str__(self):
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")


class CourseFeedback(models.Model):
    RATING = ((5, "⭐⭐⭐⭐⭐"), (4, "⭐⭐⭐⭐"), (3, "⭐⭐⭐"), (2, "⭐⭐"), (1, "⭐"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_("Course"))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name=_("User"))
    feedback = models.TextField(default=_("No feedback"), verbose_name=_("Feedback"))
    rating = models.SmallIntegerField(choices=RATING, default=5, verbose_name=_("Rating"))
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.course} ({self.user})"


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Lesson number")
    title = models.CharField(max_length=256, verbose_name="Name")
    description = models.TextField(verbose_name="Description", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="As markdown", default=False)

    def __str__(self):
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")
        ordering = ('course', 'num')


class CoursesTeacher(BaseModel):
    courses = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name="Name")
    name_second = models.CharField(max_length=128, verbose_name="Surname")
    day_birth = models.DateField(verbose_name="Birth date")
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
