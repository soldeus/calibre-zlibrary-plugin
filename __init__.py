store_version = 8

__license__ = 'GPLv3'
__copyright__ = '2024, sol <soldeus8@proton.me>'
__docformat__ = 'restructuredtext en'

from calibre.customize import StoreBase

class ZLibraryStore(StoreBase):
    name = 'Z-Library'
    description = "a z-library plugin that works."
    author = 'so1'
    version = (1, 0, 0)
    drm_free_only = True
    #formats = ['EPUB', 'PDF', 'DJVU', 'FB2', 'TXT', 'RAR', 'MOBI', 'LIT', 'DOC', 'RTF']
    formats = ['EPUB', 'PDF', 'MOBI']
    actual_plugin = 'calibre_plugins.store_zlibrary.zlibrary_plugin:ZLibraryStorePlugin'
