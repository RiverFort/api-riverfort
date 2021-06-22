from rest_framework import serializers
from .models import Account_Manager, Company_Profile, Company_Quote, Company_Trading

class Account_Manager_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Account_Manager
    fields = '__all__'

class Company_Profile_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Company_Profile
    fields = '__all__'

class Company_Profile_Ticker_Name_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Company_Profile
    fields = ['company_ticker', 'company_name']

class Company_Quote_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Company_Quote
    fields = '__all__'

class Company_Trading_Serializer(serializers.ModelSerializer):
  class Meta:
    model = Company_Trading
    fields = '__all__'

class Companies_Quotes_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  company_name   = serializers.CharField(max_length=100)
  exchange       = serializers.CharField(max_length=100)
  exchange_type  = serializers.CharField(max_length=25)
  currency       = serializers.CharField(max_length=5)
  industry       = serializers.CharField(max_length=100)
  sector         = serializers.CharField(max_length=100)
  isin           = serializers.CharField(max_length=50)
  country        = serializers.CharField(max_length=50)
  normalizer     = serializers.IntegerField()
  am_uid         = serializers.CharField()
  created_date   = serializers.DateTimeField()
  market_cap     = serializers.FloatField()
  price          = serializers.FloatField()
  timestamp      = serializers.DateTimeField()

class Companies_Quotes_Trading_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  company_name   = serializers.CharField(max_length=100)
  exchange       = serializers.CharField(max_length=100)
  exchange_type  = serializers.CharField(max_length=25)
  currency       = serializers.CharField(max_length=5)
  industry       = serializers.CharField(max_length=100)
  sector         = serializers.CharField(max_length=100)
  isin           = serializers.CharField(max_length=50)
  country        = serializers.CharField(max_length=50)
  normalizer     = serializers.IntegerField()
  am_uid         = serializers.CharField()
  created_date   = serializers.DateTimeField()
  market_cap     = serializers.FloatField()
  price          = serializers.FloatField()
  timestamp      = serializers.DateTimeField()
  market_date    = serializers.DateField()
  open           = serializers.FloatField()
  close          = serializers.FloatField()
  high           = serializers.FloatField()
  low            = serializers.FloatField()
  vwap           = serializers.FloatField()
  volume         = serializers.FloatField()
  change_percent = serializers.FloatField()

class Companies_Quotes_Trading_ADTV_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  company_name   = serializers.CharField(max_length=100)
  exchange       = serializers.CharField(max_length=100)
  exchange_type  = serializers.CharField(max_length=25)
  currency       = serializers.CharField(max_length=5)
  industry       = serializers.CharField(max_length=100)
  sector         = serializers.CharField(max_length=100)
  isin           = serializers.CharField(max_length=50)
  country        = serializers.CharField(max_length=50)
  normalizer     = serializers.IntegerField()
  am_uid         = serializers.CharField()
  created_date   = serializers.DateTimeField()
  market_cap     = serializers.FloatField()
  price          = serializers.FloatField()
  timestamp      = serializers.DateTimeField()
  market_date    = serializers.DateField()
  open           = serializers.FloatField()
  close          = serializers.FloatField()
  high           = serializers.FloatField()
  low            = serializers.FloatField()
  vwap           = serializers.FloatField()
  volume         = serializers.FloatField()
  change_percent = serializers.FloatField()
  date           = serializers.DateField()
  adtv           = serializers.FloatField()
  adtv5          = serializers.FloatField()
  adtv10         = serializers.FloatField()
  adtv20         = serializers.FloatField()
  adtv60         = serializers.FloatField()
  adtv120        = serializers.FloatField()
  isoutlier      = serializers.BooleanField()
  aadtv          = serializers.FloatField()
  aadtv5         = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv10        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv20        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv60        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv120       = serializers.DecimalField(max_digits=19, decimal_places=0)

class ADTV20_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  date           = serializers.DateField()
  adtv20         = serializers.FloatField()

class ADTV60_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  date           = serializers.DateField()
  adtv60         = serializers.FloatField()

class AADTV_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  date           = serializers.DateField()
  aadtv          = serializers.FloatField()
  aadtv5         = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv10        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv20        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv60        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv120       = serializers.DecimalField(max_digits=19, decimal_places=0)

class Quote_v2_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  currency       = serializers.CharField(max_length=5)
  market_date    = serializers.DateField()
  open           = serializers.FloatField()
  close          = serializers.FloatField()
  high           = serializers.FloatField()
  low            = serializers.FloatField()
  vwap           = serializers.FloatField()
  volume         = serializers.FloatField()
  market_cap     = serializers.FloatField()

class ADTV_AADTV_v2_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  date           = serializers.DateField()
  adtv           = serializers.FloatField()
  adtv5          = serializers.FloatField()
  adtv10         = serializers.FloatField()
  adtv20         = serializers.FloatField()
  adtv60         = serializers.FloatField()
  adtv120        = serializers.FloatField()
  isoutlier      = serializers.BooleanField()
  aadtv          = serializers.FloatField()
  aadtv5         = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv10        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv20        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv60        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv120       = serializers.DecimalField(max_digits=19, decimal_places=0)

class ADTV_v2_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  date           = serializers.DateField()
  adtv           = serializers.FloatField()
  adtv5          = serializers.FloatField()
  adtv10         = serializers.FloatField()
  adtv20         = serializers.FloatField()
  adtv60         = serializers.FloatField()
  adtv120        = serializers.FloatField()
  isoutlier      = serializers.BooleanField()

class AADTV_v2_Serializer(serializers.Serializer):
  company_ticker = serializers.CharField(max_length=25)
  date           = serializers.DateField()
  aadtv          = serializers.FloatField()
  aadtv5         = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv10        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv20        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv60        = serializers.DecimalField(max_digits=19, decimal_places=0)
  aadtv120       = serializers.DecimalField(max_digits=19, decimal_places=0)
  isoutlier      = serializers.BooleanField()
