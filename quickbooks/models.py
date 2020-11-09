from django.db import models
from mesika_utils.RandomTransactionIds import generate_sso_token


class CorporateInformation(models.Model):

    corporate_uuid = models.CharField(max_length=250, primary_key=True, unique=True,
                                      default=generate_sso_token)
    corporate = models.CharField(max_length=50)
    status = models.CharField(max_length=80, default="ACTIVE")
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return "%s %s" % (self.corporate, self.status)

    def get_details(self):

        det = {
            "quickbooks_interface_uuid": self.corporate_uuid,
            "corporate": self.corporate,

            "erp_status": self.status,

            "date_created": self.date_created.strftime("%B %d,%Y,%-I:%M %p"),
            "last_update": self.date_updated.strftime("%B %d,%Y,%-I:%M %p")
        }

        return det


class QuickBooksToken(models.Model):

    token_uuid = models.CharField(max_length=250, primary_key=True, unique=True,
                                  default=generate_sso_token)
    corporate = models.ForeignKey(CorporateInformation, on_delete=models.CASCADE, related_name="erp_uuid")

    refresh_token = models.CharField(max_length=100)
    access_token = models.TextField(max_length=3000)
    token_type = models.CharField(max_length=100)
    access_token_expire = models.CharField(max_length=100)
    refresh_token_expire = models.CharField(max_length=100)
    # id_token = models.CharField(max_length=100)
    realm_id = models.CharField(max_length=100)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return "%s %s" % (self.corporate, self.access_token)

    def get_details(self):

        det = {
            "token_uuid": self.token_uuid,
            "corporate": self.corporate.get_details(),
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "token_type": self.token_type,
            "access_token_expire": self.access_token_expire,
            # "id_token": self.id_token,
            "date_created": self.date_created.strftime("%B %d,%Y,%-I:%M %p"),
            "last_update": self.date_updated.strftime("%B %d,%Y,%-I:%M %p")
        }

        return det
    
class TextAnsibleMigrationsTry(models.Model):

    ansible_test = models.CharField(max_length=250, primary_key=True, unique=True,
                                  default=generate_sso_token)
    test_testing = models.ForeignKey(CorporateInformation, on_delete=models.CASCADE, related_name="testing")
    
    testing = models.CharField(max_length=100)
    
    def __str__(self):
        return "%s %s" % (self.testing, self.test_testing)
