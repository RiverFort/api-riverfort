class AuthRouter:
    """
    A router to control all database operations on models in the
    users applications.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read users models go to auth_db.
        """
        if model._meta.app_label == 'users':
            return 'auth_db'
        return None
    
    def db_for_write(self, model, **hints):
        """
        Attempts to write users models go to auth_db.
        """
        if model._meta.app_label == 'users':
            return 'auth_db'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the users apps only appear in the
        'auth_db' database.
        """
        if app_label == 'users':
            return db == 'auth_db'
        return None