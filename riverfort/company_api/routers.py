class CompanyRouter:
    """
    A router to control all database operations on models in the
    compang_api applications.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read company_api models go to company_db.
        """
        if model._meta.app_label == 'company_api':
            return 'company_db'
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
      if app_label == 'company_api':
            return False
      return None