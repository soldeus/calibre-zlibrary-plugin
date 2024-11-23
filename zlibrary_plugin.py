import sys, os
import urllib.parse

from calibre import browser
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.web_store_dialog import WebStoreDialog

from calibre_plugins.store_zlibrary.zlibrary_api import ZLibrary


base_url = "https://1lib.sk"

br = browser()
zlibrary = ZLibrary(
    browser=br,
    email="PLACEHOLDER@EMAIL.COM",
    password="PLACEHOLDER"
)

def search_zlib(query, extensions=["epub"], max_results=10, timeout=60):
    results = zlibrary.search(
        message=query,
        extensions=extensions,
        limit=max_results,
    )
    for book in results["books"]:
        s = SearchResult()
        s.cover_url   = book["cover"]
        s.title       = book["title"]
        s.author      = book["author"]
        s.price       = '$0.00'
        s.detail_item = book["dl"] + "+++++" +  book["href"]
        s.drm         = SearchResult.DRM_UNLOCKED
        s.formats = book["extension"].upper()

        yield s

class ZLibraryStorePlugin(BasicStoreConfig, StorePlugin):

    def create_browser(self):
        return br

    def open(self, parent=None, detail_item=None, external=False):
        href = detail_item.split("+++++")[1] if detail_item else ""
        url = base_url + href

        if external or self.config.get("open_external", False):
            open_url(url)
        else:
            d = WebStoreDialog(self.gui, base_url, parent, url, create_browser=self.create_browser)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get("tags", ""))
            d.exec_()
        
    @staticmethod
    def get_details(search_result, retries=3):
        s = search_result
        s.downloads[s.formats] = base_url + s.detail_item.split("+++++")[0]

    @staticmethod
    def search(query, max_results=10, timeout=60):
        yield from search_zlib(query, max_results=max_results, timeout=timeout)

if __name__ == '__main__':
    for result in search_zlib(' '.join(sys.argv[1:])):
        print(result)