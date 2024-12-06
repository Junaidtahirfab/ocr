from django.db import models
from account.models import Company,User
# Create your models here.



class Folder(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="folders")
    parent_folder = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name="subfolders"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    
class CompanyFile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="files")
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name="files")
    file = models.FileField(upload_to="company_files/")
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_files")
    shared_with = models.ManyToManyField(User, related_name="shared_files", blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name