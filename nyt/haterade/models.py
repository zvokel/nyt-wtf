from django.db import models
import json


class LoggedRequest(models.Model):
    time = models.DateTimeField(auto_now=True)
    ip = models.GenericIPAddressField()
    endpoint = models.CharField(max_length=1)
    agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{0}: {1} ({2})".format(str(self.time), str(self.ip), self.endpoint)

# Create your models here.
class Wordle(models.Model):
    date = models.DateField()
    word = models.CharField(max_length=5)

    def __str__(self):
        return self.word

class SpellingBee(models.Model):
    date = models.DateField()
    words = models.JSONField()

    def __str__(self):
        return json.dumps(self.words)

class Sudoku(models.Model):
    date = models.DateField()
    boards = models.JSONField()

    def __str__(self):
        return json.dumps(self.boards)

class Strands(models.Model):
    date = models.DateField()
    solution = models.JSONField()

    def __str__(self):
        return json.dumps(self.solution)


class Connections(models.Model):
    date = models.DateField()
    solution = models.JSONField()

    def __str__(self):
        return json.dumps(self.solution)

