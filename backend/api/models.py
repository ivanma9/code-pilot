from django.db import models

class Suggestion(models.Model):
    text = models.TextField()
    context = models.JSONField(null=True, blank=True)
    language = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion: {self.text[:50]}..."

class Composition(models.Model):
    message = models.TextField()
    context = models.JSONField(null=True, blank=True)
    code = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Composition: {self.message[:50]}..."