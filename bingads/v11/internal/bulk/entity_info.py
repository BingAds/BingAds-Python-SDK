class _EntityInfo:
    def __init__(self, create_func, delete_all_column_name=None, create_identifier_func=None):
        self.create_func = create_func
        self.delete_all_column_name = delete_all_column_name
        self.create_identifier_func = create_identifier_func
