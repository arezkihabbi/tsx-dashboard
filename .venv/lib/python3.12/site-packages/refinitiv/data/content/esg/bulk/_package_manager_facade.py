from ._package_manager import create_manager
from ...._tools import cached_property


class PackageManager:
    """
    Defines the package of ESG data to retrieve bulk feeds from the Refinitiv Data Platform.
    """

    def __init__(self, package_name, session=None) -> None:
        self.package_name = package_name
        self.session = session

    @cached_property
    def _manager(self):
        return create_manager(self.package_name, self.session)

    def update_files(self) -> None:
        """Downloads the latest init and delta files of ESG package data and uncompresses them."""
        self._manager.update_files()

    def reset_files(self) -> None:
        """Resets all the previously downloaded local files that belong to particular ESG data package."""
        self._manager.reset_files()

    def cleanup_files(self) -> None:
        """Cleans up all the previously downloaded local files that belong to a particular ESG data package."""
        self._manager.cleanup_files()

    def cleanup_db(self) -> None:
        """Cleans up the local in-memory database of particular ESG data that was previously created."""
        self._manager.cleanup_db()

    def update_db(self) -> None:
        """Updates a local in-memory database with the latest downloaded files."""
        self._manager.update_db()
