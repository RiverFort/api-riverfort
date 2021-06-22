from django.urls import path
from . import views

urlpatterns = [
  path("companies-full-list-search/",                     views.companies_full_list_search,        name="companies-full-list-search"),
  path("industries-full-list-search/",                    views.industries_full_list_search,       name="industries-full-list-search"),

  path("companies-full-list/",                            views.companies_full_list,               name="companies-full-list"),
  path("companies-full-list/exchange/<str:exchange>/",    views.companies_full_list_exchange,      name="companies-full-list-exchange"),
  path("companies-full-list/country/<str:country_code>/", views.companies_full_list_country,       name="companies-full-list-country"),
  
  path("companies-full-list/region/asia-pacific",         views.companies_full_list_asia_pacific,  name="companies-full-list-asia-pacific"),
  path("companies-full-list/region/africa",               views.companies_full_list_africa,        name="companies-full-list-africa"),
  path("companies-full-list/region/europe",               views.companies_full_list_europe,        name="companies-full-list-europe"),
  path("companies-full-list/region/north-america",        views.companies_full_list_north_america, name="companies-full-list-north-america"),
  path("companies-full-list/region/south-america",        views.companies_full_list_south_america, name="companies-full-list-south-america"),

  path("adtv20/<str:company_ticker>/",                    views.adtv20,                            name="adtv20"),
  path("adtv60/<str:company_ticker>/",                    views.adtv60,                            name="adtv60"),

  # filters:
  path("companies-full-list/filter/industry/<str:industry>/",                                                                                    views.companies_full_list_industry,                        name="companies-full-list-industry"),
  path("companies-full-list/filter/mktcap/<str:mktcapMin>/<str:mktcapMax>/",                                                                     views.companies_full_list_mktcap,                          name="companies-full-list-mktcap"),
  path("companies-full-list/filter/adtv20/<str:adtv20>/",                                                                                        views.companies_full_list_adtv20,                          name="companies-full-list-adtv20"),
  
  path("companies-full-list/filter/exchange-industry/<str:exchange>/<str:industry>/",                                                            views.companies_full_list_exchange_industry,               name="companies-full-list-exchange-industry"),
  path("companies-full-list/filter/exchange-mktcap/<str:exchange>/<str:mktcapMin>/<str:mktcapMax>/",                                             views.companies_full_list_exchange_mktcap,                 name="companies-full-list-exchange-mktcap"),
  path("companies-full-list/filter/exchange-adtv20/<str:exchange>/<str:adtv20>/",                                                                views.companies_full_list_exchange_adtv20,                 name="companies-full-list-exchange-adtv20"),
  
  path("companies-full-list/filter/industry-mktcap/<str:industry>/<str:mktcapMin>/<str:mktcapMax>/",                                             views.companies_full_list_industry_mktcap,                 name="companies-full-list-industry-mktcap"),
  path("companies-full-list/filter/industry-adtv20/<str:industry>/<str:adtv20>/",                                                                views.companies_full_list_industry_adtv20,                 name="companies-full-list-industry-adtv20"),
  path("companies-full-list/filter/industry-mktcap-adtv20/<str:industry>/<str:mktcapMin>/<str:mktcapMax>/<str:adtv20>/",                         views.companies_full_list_industry_mktcap_adtv20,          name="companies-full-list-industry-mktcap-adtv20"),

  path("companies-full-list/filter/exchange-industry-mktcap/<str:exchange>/<str:industry>/<str:mktcapMin>/<str:mktcapMax>/",                     views.companies_full_list_exchange_industry_mktcap,        name="companies-full-list-exchange-industry-mktcap"),
  path("companies-full-list/filter/exchange-industry-adtv20/<str:exchange>/<str:industry>/<str:adtv20>/",                                        views.companies_full_list_exchange_industry_adtv20,        name="companies-full-list-exchange-industry-adtv20"),
  path("companies-full-list/filter/exchange-industry-mktcap-adtv20/<str:exchange>/<str:industry>/<str:mktcapMin>/<str:mktcapMax>/<str:adtv20>/", views.companies_full_list_exchange_industry_mktcap_adtv20, name="companies-full-list-exchange-industry-mktcap-adtv20"),
  
  path("companies-full-list/filter/mktcap-adtv20/<str:mktcapMin>/<str:mktcapMax>/<str:adtv20>/",                                                 views.companies_full_list_mktcap_adtv20,                   name="companies-full-list-mktcap-adtv20"),

  










  path("companies-all/",               views.companies_all,     name="companies-all"),
  path("companies-all-no-pagination/", views.companies_all_no_pagination, name="companies-all-no-pagination"),
  path("companies-all/csv",            views.companies_all_csv, name="companies-all-csv"),

  path("exchange/<str:exchange>/",    views.companies_exchange,     name="exchange"),
  path("exchange/<str:exchange>/csv", views.companies_exchange_csv, name="exchange-csv"),

  path("country/<str:country_code>/",    views.companies_country,     name="country"),
  path("country/<str:country_code>/csv", views.companies_country_csv, name="country-csv"),

  path("region/asia-pacific",    views.companies_asia_pacific,     name="asia-pacific"),
  path("region/africa",          views.companies_africa,           name="africa"),
  path("region/europe",          views.companies_europe,           name="europe"),
  path("region/north-america",   views.companies_north_america,    name="north-america"),
  path("region/south-america",   views.companies_south_america,    name="south-america"),

  path("region/asia-pacific/csv",  views.companies_asia_pacific_csv,  name="asia-pacific-csv"),
  path("region/africa/csv",        views.companies_africa_csv,        name="africa-csv"),
  path("region/europe/csv",        views.companies_europe_csv,        name="europe-csv"),
  path("region/north-america/csv", views.companies_north_america_csv, name="north-america-csv"),
  path("region/south-america/csv", views.companies_south_america_csv, name="south-america-csv"),

  path("company-detail/<str:company_ticker>/", views.company_all_data, name="company_all_data"),
  path("profile/<str:company_ticker>/",        views.company,          name="profile"),
  path("quote/<str:company_ticker>/",          views.company_quote,    name="quote"),
  path("trading/<str:company_ticker>/",        views.trading_all,      name="trading-all"),
  path("trading-recent/<str:company_ticker>/", views.trading_recent,   name="trading-recent"),
  
  path("aadtv/<str:company_ticker>/",          views.aadtv,            name="aadtv"),





  path("companies/",                            views.companies,        name="companies"),
  path("companies-quote/",                      views.companies_quote,  name="companies-quote"),
  path("companies-quotes/",                     views.companies_quotes, name="companies-quotes"),
  path("companies-quotes-trading/",             views.companies_quotes_recent_trading, name="companies-quotes-trading"),
  path("account-manager/<str:name>",            views.account_manager,  name="account-manager"),
  path("account-managers/",                     views.account_managers, name="account-managers"),







  # mobile agents:
  path("v2/quote/<str:company_ticker>/", views.quote_v2, name="quote_v2"),
  path("v2/recent-adtv-aadtv/<str:company_ticker>/", views.recent_adtv_aadtv_v2, name="recent_adtv_aadtv_v2"),
  path("v2/recent-adtv/<str:company_ticker>/", views.recent_adtv_v2, name="recent_adtv_v2"),
  path("v2/recent-aadtv/<str:company_ticker>/", views.recent_aadtv_v2, name="recent_aadtv_v2"),

]