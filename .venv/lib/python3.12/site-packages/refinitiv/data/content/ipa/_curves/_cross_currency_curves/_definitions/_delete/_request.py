from ....._object_definition import ObjectDefinition


class DeleteRequest(ObjectDefinition):
    """
    Delete a cross currency curve definition

    Parameters
    ----------
    id : str
        The identifier of the cross currency definition.
    """

    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id

    @property
    def id(self):
        """
        :return: str
        """
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)
