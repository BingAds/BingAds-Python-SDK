class _ErrorMessages:
    @staticmethod
    def get_format_version_not_supported_message(version):
        return "Format version {0} is not supported".format(version)

    @staticmethod
    def get_property_must_not_be_null_message(entity_type, property_name):
        return "Property {0}.{1} must not be null when calling WriteEntity.".format(str(entity_type),
                                                                                    str(property_name))

    @staticmethod
    def get_list_must_not_be_null_or_empty(entity_type, property_name):
        return "List {0}.{1} must not be null or empty when calling WriteEntity.".format(str(entity_type),
                                                                                         str(property_name))
