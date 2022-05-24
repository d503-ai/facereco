# ---- coding: utf-8 ----
# ===================================================
# Author: Susanta Biswas
# ===================================================
"""Description: Class to handle saving and retrieving facial data.
The data is saved on disk for peersistence, also an in-memory cache is 
used for quicker look ups.

For persistent storage a JSON file is used and for in memory cache,
native python set is used.
Cache doesn't allow duplicates. Without duplicates, entries for 
search are limited.

Cache is initialized with data loaded from DB. Then each addition 
of face data for a new user goes through two writes:
1. Addition to cache
2. Saved to disk DB.

Cache is always up to date with the latest facial data.

Usage: python -m face_recog.face_data_store
"""
# ===================================================

from .exceptions import DatabaseFileNotFound, InvalidCacheInitializationData
from .json_persistent_storage import JSONStorage
from .simple_cache import SimpleCache


class FaceDataStore:
    """Class to handle saving and retrieving facial data.
    The data is saved on disk for peersistence, also an in-memory cache is
    used for quicker look ups.

    For persistent storage a JSON file is used and for in memory cache,
    native python set is used.
    Cache doesn't allow duplicates. Without duplicates, entries for
    search are limited.

    Cache is initialized with data loaded from DB. Then each addition
    of face data for a new user goes through two writes:
    1. Addition to cache
    2. Saved to disk DB.

    Cache is always up to date with the latest facial data.
    """

    def __init__(self, persistent_data_loc="data/facial_data.json") -> None:
        # persistent storage handler
        self.db_handler = JSONStorage(persistent_data_loc)
        saved_data = []
        try:
            # Initialize the cache handler with data from DB
            saved_data = self.db_handler.get_all_data()
        except DatabaseFileNotFound:
            pass
        try:
            self.cache_handler = SimpleCache(saved_data)
        except InvalidCacheInitializationData:
            raise InvalidCacheInitializationData

    def add_facial_data(self, facial_data):
        """Add facial data to the in memory cache and
        persistent storage.

        Args:
            facial_data (Dict): {'id':str, 'encoding':tuple(), 'name':str}
        """
        # add to cache and save on disk
        self.cache_handler.add_data(face_data=facial_data)
        self.db_handler.add_data(face_data=facial_data)

    def remove_facial_data(self, face_id: str = None):
        """Delete facial record with the matching face id.

        Args:
            face_id (str, optional): Face data identifier. Defaults to None.
        """
        self.cache_handler.delete_data(face_id=face_id)
        self.db_handler.delete_data(face_id=face_id)

    def get_all_facial_data(self):
        """Returns data of all the registered faces.

        Returns:
            List[Dict]: List of facial data
        """
        # Cache data is returned since it is always up to date
        # with CRUD operations.
        return self.cache_handler.get_all_data()
