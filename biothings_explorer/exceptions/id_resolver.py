class InvalidIDResolverInputError(Exception):
    """Exception raised for errors in the input to ID Resolver class.

    Attributes:
        input_ids -- input ids which caused the error
        message -- explanation of the error
    """

    def __init__(self, input_ids, message="Your Input to ID Resolver is Invalid"):
        self.input_ids = input_ids
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.input_ids} -> {self.message}"

