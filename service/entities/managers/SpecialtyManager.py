from django.db import models


class SpecialtyManager(models.Manager):
    def exists_by_parent(self, parent):
        return self.filter(parent=parent).exists()

    def by_name_starting_with(self, name):
        return self.filter(name__startswith=name)

    def by_parent_id(self, parent_id):
        return self.filter(parent_id=parent_id)
