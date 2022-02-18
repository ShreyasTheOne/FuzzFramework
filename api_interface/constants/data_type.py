class DataTypeNotAccepted(Exception):
    """
    Raised when data type is not accepted
    """

    def __init__(self, invalid_data_type):
        self.invalid_data_type = invalid_data_type
    
    def __str__(self):
        return f"Unrecognised or unaccepted data type {self.invalid_data_type}"


class DataType:
    """
    Defines the accepted types of payload data types
    """

    DATA_TYPES = (
        ('int', int),
        ('str', str),
        ('list', list),
        ('dict', dict),
        ('bool', bool),
        ('None', None),
    )

    @classmethod
    def get_data_type(cls, data_type):
        """
        Return data type if exists, else raise error

        :param data_type: String representation of data type
        :return: Python data type corresponding to param data_type
        """

        for tup in cls.DATA_TYPES:
            if data_type == tup[0]:
                return tup[1]
        
        raise DataTypeNotAccepted(data_type)
