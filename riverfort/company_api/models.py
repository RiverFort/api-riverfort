from django.db import models

class Account_Manager(models.Model):
  am_uid    = models.AutoField(primary_key=True)
  am_name   = models.CharField(max_length=100)
  am_email  = models.CharField(max_length=100)
  am_mobile = models.CharField(max_length=20)

  def __str__(self):
    return self.am_name

  class Meta:
    db_table = 'account_manager'
    app_label = 'company_api'

class Company_Profile(models.Model):
  company_ticker = models.CharField(primary_key=True, max_length=25)
  company_name   = models.CharField(max_length=100)
  exchange       = models.CharField(max_length=100)
  exchange_type  = models.CharField(max_length=25)
  currency       = models.CharField(max_length=5)
  industry       = models.CharField(max_length=100)
  sector         = models.CharField(max_length=100)
  isin           = models.CharField(max_length=50)
  country        = models.CharField(max_length=50)
  normalizer     = models.IntegerField()
  am_uid         = models.ForeignKey(
      Account_Manager, 
      db_column='am_uid', 
      on_delete=models.CASCADE,
  )
  created_date   = models.DateTimeField()

  class Meta:
        db_table = 'company_profile'
        app_label = 'company_api'

class Company_Quote(models.Model):
  company_ticker = models.OneToOneField(
      Company_Profile,
      db_column='company_ticker',
      on_delete=models.CASCADE,
      primary_key=True,
  )
  market_cap     = models.FloatField()
  price          = models.FloatField()
  timestamp      = models.DateTimeField()

  class Meta:
    db_table = 'company_quote'
    app_label = 'company_api'

class Company_Trading(models.Model):
  company_ticker = models.OneToOneField(
      Company_Profile,
      db_column='company_ticker',
      on_delete=models.CASCADE,
      primary_key=True,
  )
  market_date    = models.DateField()
  open           = models.FloatField()
  close          = models.FloatField()
  high           = models.FloatField()
  low            = models.FloatField()
  vwap           = models.FloatField()
  volume         = models.FloatField()
  change_percent = models.FloatField()

  class Meta:
    db_table = 'company_trading'
    app_label = 'company_api'

# mobile agent
