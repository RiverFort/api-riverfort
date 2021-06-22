from rest_framework.decorators import api_view
from rest_framework.response   import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import Account_Manager_Serializer, Company_Profile_Serializer, Company_Quote_Serializer, Company_Trading_Serializer, Companies_Quotes_Serializer, Companies_Quotes_Trading_Serializer, Companies_Quotes_Trading_ADTV_Serializer, ADTV20_Serializer, ADTV60_Serializer, AADTV_Serializer, Company_Profile_Ticker_Name_Serializer, Quote_v2_Serializer, ADTV_AADTV_v2_Serializer, ADTV_v2_Serializer, AADTV_v2_Serializer
from .models      import Account_Manager, Company_Profile, Company_Quote, Company_Trading


import csv
import datetime
from django.http import HttpResponse



from rest_framework.views import APIView
from rest_framework import generics


from psycopg2.extensions import AsIs

# Create your views here.

@api_view(['GET'])
def company(request, company_ticker):
  company    = Company_Profile.objects.get(company_ticker=company_ticker)
  serializer = Company_Profile_Serializer(company, many=False)
  return Response(serializer.data)

@api_view(['GET'])
def company_quote(request, company_ticker):
  company_quote = Company_Quote.objects.get(company_ticker=company_ticker)
  serializer    = Company_Quote_Serializer(company_quote, many=False)
  return Response(serializer.data)





@api_view(['GET'])
def companies(request):
  companies  = Company_Profile.objects.all()
  serializer = Company_Profile_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_quote(request):
  companies  = Company_Quote.objects.all()
  serializer = Company_Quote_Serializer(companies, many=True)
  return Response(serializer.data)


@api_view(['GET'])
def constituents(request, exchange):
  constituents  = Company_Profile.objects.filter(exchange=exchange)
  serializer    = Company_Profile_Serializer(constituents, many=True)
  return Response(serializer.data)


@api_view(['GET'])
def account_manager(request, name):
  account_manager = Account_Manager.objects.filter(am_name=name)
  serializer      = Account_Manager_Serializer(account_manager, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def account_managers(request):
  account_managers = Account_Manager.objects.all()
  serializer       = Account_Manager_Serializer(account_managers, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_quotes(request):
  companies  = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker')
  serializer = Companies_Quotes_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_quotes_recent_trading(request):
  companies  = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker;')
  serializer = Companies_Quotes_Trading_Serializer(companies, many=True)
  return Response(serializer.data)










# class CompanyList(generics.ListAPIView):
#   # queryset = Company_Profile.objects.all()
#   # serializer_class = Company_Profile_Serializer
#   queryset = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY company_profile.company_ticker;')
#   serializer_class = Companies_Quotes_Trading_ADTV_Serializer
#   filter_backends = [filters.OrderingFilter]
#   ordering_fields = ['company_ticker', 'company_name']



# class ListCompanies(APIView):
#   def filter_queryset(self, queryset):
#     for backend in list(self.filter_backends):
#       queryset = backend().filter_queryset(self.request, queryset, self)
#     return queryset

#   def get(self, request, format=None):
#     # companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY company_profile.company_ticker;')
#     # serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
#     # return Response(serializer.data)
#     paginator = PageNumberPagination()
#     paginator.page_size = 10
#     companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY company_profile.company_ticker;')
#     result_page = paginator.paginate_queryset(companies, request)
#     serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)










# all companies recent profile, quote, trading, and adtv
@api_view(['GET'])
def companies_full_list(request):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY company_profile.company_ticker;')
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY %s %s;', [AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_exchange(request, exchange):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s ORDER BY company_profile.company_ticker;', [exchange])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s ORDER BY %s %s;', [exchange, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_country(request, country_code):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  if country_code == 'GB':
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('GB', 'United Kingdom') ORDER BY company_profile.company_ticker;")
  elif country_code == 'CA':
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('CA', 'Canada') ORDER BY company_profile.company_ticker;")
  elif country_code == 'AU':
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AU', 'Australia') ORDER BY company_profile.company_ticker;")
  elif country_code == 'FR':
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('FR', 'France') ORDER BY company_profile.company_ticker;")
  elif country_code == 'MU':
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('MU', 'Mauritius') ORDER BY company_profile.company_ticker;")
  else:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country=%s ORDER BY company_profile.company_ticker;', [country_code])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country=%s ORDER BY %s %s;', [country_code, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_asia_pacific(request):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AZ', 'AU', 'BD', 'CN', 'CY', 'HK', 'IN', 'IL', 'KR', 'MY', 'MN', 'NZ', 'PG', 'SG', 'SB', 'TH', 'AE', 'Australia', 'Mongolia', 'New Zealand', 'Taiwan') ORDER BY company_profile.company_ticker;")
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AZ', 'AU', 'BD', 'CN', 'CY', 'HK', 'IN', 'IL', 'KR', 'MY', 'MN', 'NZ', 'PG', 'SG', 'SB', 'TH', 'AE', 'Australia', 'Mongolia', 'New Zealand', 'Taiwan') ORDER BY %s %s;", [AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_africa(request):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('MU', 'NG', 'ZA', 'TG', 'ZM', 'Mauritius') ORDER BY company_profile.company_ticker;")
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('MU', 'NG', 'ZA', 'TG', 'ZM', 'Mauritius') ORDER BY %s %s;", [AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_europe(request):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AT', 'BE', 'DK', 'FI', 'FR', 'DE', 'GI', 'GG', 'IE', 'IM', 'IT', 'JE', 'LU', 'MT', 'NL', 'NO', 'PL', 'RU', 'ES', 'SE', 'CH', 'UA', 'France', 'Ireland', 'Isle of Man', 'Jersey', 'Sweden', 'Switzerland') ORDER BY company_profile.company_ticker;")
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AT', 'BE', 'DK', 'FI', 'FR', 'DE', 'GI', 'GG', 'IE', 'IM', 'IT', 'JE', 'LU', 'MT', 'NL', 'NO', 'PL', 'RU', 'ES', 'SE', 'CH', 'UA', 'France', 'Ireland', 'Isle of Man', 'Jersey', 'Sweden', 'Switzerland') ORDER BY %s %s;", [AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_north_america(request):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('BM', 'VG', 'CA', 'KY', 'US', 'British Virgin Islands', 'Canada', 'Cayman Islands') ORDER BY company_profile.company_ticker;")
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('BM', 'VG', 'CA', 'KY', 'US', 'British Virgin Islands', 'Canada', 'Cayman Islands') ORDER BY %s %s;", [AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_south_america(request):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('CL', 'FK') ORDER BY company_profile.company_ticker;")
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('CL', 'FK') ORDER BY %s %s;", [AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def companies_full_list_search(request):
  companies = Company_Profile.objects.raw('SELECT company_ticker, company_name FROM company_profile ORDER BY company_ticker;')
  serializer = Company_Profile_Ticker_Name_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def industries_full_list_search(request):
  companies = Company_Profile.objects.values_list('industry', flat=True).distinct().order_by('industry')
  return Response(companies)










# Filter
@api_view(['GET'])
def companies_full_list_industry(request, industry):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s ORDER BY company_profile.company_ticker;', [industry])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s ORDER BY %s %s;', [industry, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_mktcap(request, mktcapMin, mktcapMax):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE market_cap BETWEEN %s AND %s ORDER BY company_profile.company_ticker;', [mktcapMin, mktcapMax])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE market_cap BETWEEN %s AND %s ORDER BY %s %s;', [mktcapMin, mktcapMax, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_adtv20(request, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE adtv20 < %s ORDER BY company_profile.company_ticker;', [adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE adtv20 < %s ORDER BY %s %s;', [adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_exchange_industry(request, exchange, industry):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s ORDER BY company_profile.company_ticker;', [exchange, industry])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s ORDER BY %s %s;', [exchange, industry, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_exchange_mktcap(request, exchange, mktcapMin, mktcapMax):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND (market_cap BETWEEN %s AND %s) ORDER BY company_profile.company_ticker;', [exchange, mktcapMin, mktcapMax])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND (market_cap BETWEEN %s AND %s) ORDER BY %s %s;', [exchange, mktcapMin, mktcapMax, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_exchange_adtv20(request, exchange, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND adtv20 < %s ORDER BY company_profile.company_ticker;', [exchange, adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND adtv20 < %s ORDER BY %s %s;', [exchange, adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_industry_mktcap(request, industry, mktcapMin, mktcapMax):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s AND (market_cap BETWEEN %s AND %s) ORDER BY company_profile.company_ticker;', [industry, mktcapMin, mktcapMax])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s AND (market_cap BETWEEN %s AND %s) ORDER BY %s %s;', [industry, mktcapMin, mktcapMax, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_industry_adtv20(request, industry, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s AND adtv20 < %s ORDER BY company_profile.company_ticker;', [industry, adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s AND adtv20 < %s ORDER BY %s %s;', [industry, adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_industry_mktcap_adtv20(request, industry, mktcapMin, mktcapMax, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s AND (market_cap BETWEEN %s AND %s) AND adtv20 < %s ORDER BY company_profile.company_ticker;', [industry, mktcapMin, mktcapMax, adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE industry=%s AND (market_cap BETWEEN %s AND %s) AND adtv20 < %s ORDER BY %s %s;', [industry, mktcapMin, mktcapMax, adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
def companies_full_list_exchange_industry_mktcap(request, exchange, industry, mktcapMin, mktcapMax):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s AND (market_cap BETWEEN %s AND %s) ORDER BY company_profile.company_ticker;', [exchange, industry, mktcapMin, mktcapMax])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s AND (market_cap BETWEEN %s AND %s) ORDER BY %s %s;', [exchange, industry, mktcapMin, mktcapMax, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_exchange_industry_adtv20(request, exchange, industry, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s AND adtv20 < %s ORDER BY company_profile.company_ticker;', [exchange, industry, adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s AND adtv20 < %s ORDER BY %s %s;', [exchange, industry, adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_exchange_industry_mktcap_adtv20(request, exchange, industry, mktcapMin, mktcapMax, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s AND (market_cap BETWEEN %s AND %s) AND adtv20 < %s ORDER BY company_profile.company_ticker;', [exchange, industry, mktcapMin, mktcapMax, adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s AND industry=%s AND (market_cap BETWEEN %s AND %s) AND adtv20 < %s ORDER BY %s %s;', [exchange, industry, mktcapMin, mktcapMax, adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def companies_full_list_mktcap_adtv20(request, mktcapMin, mktcapMax, adtv20):
  # pagination
  paginator = PageNumberPagination()
  paginator.page_size = 50
  # sorting and ordering
  sortParam  = request.GET.get("sort", None)
  orderParam = request.GET.get("order", None)
  # default list order by company_ticker
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE (market_cap BETWEEN %s AND %s) AND adtv20 < %s ORDER BY company_profile.company_ticker;', [mktcapMin, mktcapMax, adtv20])
  # customize list order
  if sortParam and orderParam:
    companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE (market_cap BETWEEN %s AND %s) AND adtv20 < %s ORDER BY %s %s;', [mktcapMin, mktcapMax, adtv20, AsIs(sortParam), AsIs(orderParam)])
  result_page = paginator.paginate_queryset(companies, request)
  serializer = Companies_Quotes_Trading_ADTV_Serializer(result_page, many=True)
  return paginator.get_paginated_response(serializer.data)













@api_view(['GET'])
def companies_all(request):
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY company_profile.company_ticker;')
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_all_no_pagination(request):
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker ORDER BY company_profile.company_ticker;')
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def company_all_data(request, company_ticker):
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE company_profile.company_ticker=%s;', [company_ticker])
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)


# csv: companies_all
@api_view(['GET'])
def companies_all_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker;')
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

# an exchange's companies recent profile, quote, trading and adtv
@api_view(['GET'])
def companies_exchange(request, exchange):
  companies  = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s;', [exchange])
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

# csv: companies_exchange
@api_view(['GET'])
def companies_exchange_csv(request, exchange):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE exchange=%s;', [exchange])
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

# a country's companies recent profile, quote, trading and adtv
@api_view(['GET'])
def companies_country(request, country_code):
  companies  = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country=%s;', [country_code])
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

# csv: companies_country
@api_view(['GET'])
def companies_country_csv(request, country_code):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw('SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country=%s;', [country_code])
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

# companies based on regions:
@api_view(['GET'])
def companies_asia_pacific(request):
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AZ', 'AU', 'BD', 'CN', 'CY', 'HK', 'IN', 'IL', 'KR', 'MY', 'MN', 'NZ', 'PG', 'SG', 'SB', 'TH', 'AE', 'Australia', 'Mongolia', 'New Zealand', 'Taiwan');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_africa(request):
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('MU', 'NG', 'ZA', 'TG', 'ZM', 'Mauritius');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_europe(request):
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AT', 'BE', 'DK', 'FI', 'FR', 'DE', 'GI', 'GG', 'IE', 'IM', 'IT', 'JE', 'LU', 'MT', 'NL', 'NO', 'PL', 'RU', 'ES', 'SE', 'CH', 'GB', 'UA', 'France', 'Ireland', 'Isle of Man', 'Jersey', 'Sweden', 'Switzerland', 'United Kingdom');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_north_america(request):
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('BM', 'VG', 'CA', 'KY', 'US', 'British Virgin Islands', 'Canada', 'Cayman Islands');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def companies_south_america(request):
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('CL', 'FK');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  return Response(serializer.data)

# csv: companies based on regions
@api_view(['GET'])
def companies_asia_pacific_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AZ', 'AU', 'BD', 'CN', 'CY', 'HK', 'IN', 'IL', 'KR', 'MY', 'MN', 'NZ', 'PG', 'SG', 'SB', 'TH', 'AE', 'Australia', 'Mongolia', 'New Zealand', 'Taiwan');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

@api_view(['GET'])
def companies_africa_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('MU', 'NG', 'ZA', 'TG', 'ZM', 'Mauritius');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

@api_view(['GET'])
def companies_europe_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('AT', 'BE', 'DK', 'FI', 'FR', 'DE', 'GI', 'GG', 'IE', 'IM', 'IT', 'JE', 'LU', 'MT', 'NL', 'NO', 'PL', 'RU', 'ES', 'SE', 'CH', 'GB', 'UA', 'France', 'Ireland', 'Isle of Man', 'Jersey', 'Sweden', 'Switzerland', 'United Kingdom');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

@api_view(['GET'])
def companies_north_america_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('BM', 'VG', 'CA', 'KY', 'US', 'British Virgin Islands', 'Canada', 'Cayman Islands');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response

@api_view(['GET'])
def companies_south_america_csv(request):
  response = HttpResponse(content_type='text/csv')
  response['Content-Disposition']='attachment; filename=Company List' + str(datetime.datetime.now()) + '.csv'
  writer = csv.writer(response)
  writer.writerow(['company_ticker', 'company_name', 'exchange', 'exchange_type', 'currency', 'industry', 'sector', 'isin', 'country', 'normalizer', 'created_date', 'am_uid', 'market_cap', 'price', 'timestamp', 'market_date', 'open', 'close', 'high', 'low', 'vwap', 'volume', 'change_percent', 'date', 'adtv', 'adtv5', 'adtv10', 'adtv20', 'adtv60', 'isoutlier', 'aadtv', 'aadtv5', 'aadtv10', 'aadtv20', 'aadtv60', 'aadtv120'])
  companies  = Company_Profile.objects.raw("SELECT * FROM company_profile LEFT JOIN company_quote ON company_profile.company_ticker=company_quote.company_ticker LEFT JOIN (SELECT c.company_ticker, c.market_date, c.open, c.close, c.high, c.low, c.vwap, c.volume, c.change_percent FROM company_trading c INNER JOIN (SELECT company_ticker, MAX(market_date) as MaxDate FROM company_trading GROUP BY company_ticker) cm ON c.company_ticker=cm.company_ticker AND c.market_date=cm.MaxDate) t ON company_profile.company_ticker=t.company_ticker LEFT JOIN (SELECT a.company_ticker, a.date, a.adtv, a.adtv5, a.adtv10, a.adtv20, a.adtv60, a.adtv120, a.isoutlier, a.aadtv, a.aadtv5, a.aadtv10, a.aadtv20, a.aadtv60, a.aadtv120 FROM company_adtv a INNER JOIN (SELECT company_ticker, MAX(date) as MaxDate FROM company_adtv GROUP BY company_ticker) am ON a.company_ticker=am.company_ticker AND a.date=am.MaxDate) a ON company_profile.company_ticker=a.company_ticker WHERE country IN ('CL', 'FK');")
  serializer = Companies_Quotes_Trading_ADTV_Serializer(companies, many=True)
  for company in serializer.data:
    writer.writerow([company['company_ticker'], company['company_name'], company['exchange'], company['exchange_type'], company['currency'], company['industry'], company['sector'], company['isin'], company['country'], company['normalizer'], company['created_date'], company['am_uid'], company['market_cap'], company['price'], company['timestamp'], company['market_date'], company['open'], company['close'], company['high'], company['low'], company['vwap'], company['volume'], company['change_percent'], company['date'], company['adtv'], company['adtv5'], company['adtv10'], company['adtv20'], company['adtv60'], company['isoutlier'], company['aadtv'], company['aadtv5'], company['aadtv10'], company['aadtv20'], company['aadtv60'], company['aadtv120']])
  return response
  
@api_view(['GET'])
def trading_all(request, company_ticker):
  company_trading = Company_Trading.objects.filter(company_ticker=company_ticker).order_by('market_date')
  serializer      = Company_Trading_Serializer(company_trading, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def trading_recent(request, company_ticker):
  company_trading = Company_Trading.objects.filter(company_ticker=company_ticker).order_by('-market_date').first()
  serializer      = Company_Trading_Serializer(company_trading, many=False)
  return Response(serializer.data)

@api_view(['GET'])  
def aadtv(request, company_ticker):
  adtv       = Company_Profile.objects.raw("SELECT company_ticker, date, aadtv, aadtv5, aadtv10, aadtv20, aadtv60, aadtv120 FROM company_adtv WHERE company_ticker=%s ORDER BY date;", [company_ticker])
  serializer = AADTV_Serializer(adtv, many=True)
  return Response(serializer.data)

@api_view(['GET'])  
def adtv20(request, company_ticker):
  adtv       = Company_Profile.objects.raw("SELECT company_ticker, date, adtv20 FROM company_adtv WHERE company_ticker=%s ORDER BY date;", [company_ticker])
  serializer = ADTV20_Serializer(adtv, many=True)
  return Response(serializer.data)

@api_view(['GET'])  
def adtv60(request, company_ticker):
  adtv       = Company_Profile.objects.raw("SELECT company_ticker, date, adtv60 FROM company_adtv WHERE company_ticker=%s ORDER BY date;", [company_ticker])
  serializer = ADTV60_Serializer(adtv, many=True)
  return Response(serializer.data)





# mobile agents:

@api_view(['GET'])
def quote_v2(request, company_ticker):
  quote = Company_Profile.objects.raw("""
  SELECT 
  company_profile.company_ticker, 
  company_profile.currency, 
  company_trading.market_date, 
  company_trading.open, 
  company_trading.close, 
  company_trading.high, 
  company_trading.low, 
  company_trading.vwap, 
  company_trading.volume, 
  company_quote.market_cap
  FROM company_profile 
  LEFT JOIN company_trading ON company_profile.company_ticker = company_trading.company_ticker 
  LEFT JOIN company_quote ON company_trading.company_ticker = company_quote.company_ticker 
  WHERE company_profile.company_ticker = %s 
  ORDER BY market_date DESC 
  LIMIT 1;
  """, [company_ticker])
  serializer = Quote_v2_Serializer(quote, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def recent_adtv_aadtv_v2(request, company_ticker):
  adtv = Company_Profile.objects.raw("""
  SELECT *
  FROM company_adtv 
  WHERE company_ticker=%s 
  ORDER BY date DESC
  LIMIT 1;
  """, [company_ticker])
  serializer = ADTV_AADTV_v2_Serializer(adtv, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def recent_adtv_v2(request, company_ticker):
  adtv = Company_Profile.objects.raw("""
  SELECT company_ticker, date, adtv, adtv5, adtv10, adtv20, adtv60, adtv120, isoutlier
  FROM company_adtv 
  WHERE company_ticker=%s 
  ORDER BY date DESC
  LIMIT 1;
  """, [company_ticker])
  serializer = ADTV_v2_Serializer(adtv, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def recent_aadtv_v2(request, company_ticker):
  adtv = Company_Profile.objects.raw("""
  SELECT company_ticker, date, aadtv, aadtv5, aadtv10, aadtv20, aadtv60, aadtv120, isoutlier
  FROM company_adtv 
  WHERE company_ticker=%s 
  ORDER BY date DESC
  LIMIT 1;
  """, [company_ticker])
  serializer = AADTV_v2_Serializer(adtv, many=True)
  return Response(serializer.data)