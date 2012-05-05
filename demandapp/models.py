from django.db import models

class SiteManager(models.Manager):
    def top(self):
        return self.get_query_set().annotate(
            vote_count=models.Count('vote')).order_by('-vote_count')

    def new(self):
        return self.get_query_set().order_by('-date')[:10]

class Site(models.Model):
    domain = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now_add=True)

    support_browserid = models.BooleanField(default=False)

    objects = SiteManager()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.domain

        super(Site, self).save(*args, **kwargs)

    def votes(self):
        return self.vote_set.count()

    def get_vote_url(self):
        return u'/demand/%s/' % self.domain

    def get_absolute_url(self):
        return u'/%s/' % self.domain

class Vote(models.Model):
    website = models.ForeignKey(Site)
    voter = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('website', 'voter')

