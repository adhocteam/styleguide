"""Check the built site's F-08 assets and existing Brand redirects."""

import functools
import re
import threading
import unittest
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import unquote, urlsplit
from urllib.request import urlopen


SITE = Path(__file__).resolve().parents[1] / "_site"
BRAND = "https://brand.adhoc.team/"
JQUERY_VERSION = re.compile(r"jQuery(?: JavaScript Library)?\s+v?(\d+)\.(\d+)\.(\d+)", re.I)


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.redirects = []
        self.scripts = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.redirects.append(attrs.get("content", ""))
        if tag == "script" and attrs.get("src"):
            self.scripts.append(attrs["src"])


class PublishedAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {path: Page(path.read_text()) for path in SITE.rglob("*.html")}
        if SITE.joinpath("index.html") not in cls.pages:
            raise RuntimeError("Build the site with bundle exec jekyll build before running these checks.")

    def test_every_page_keeps_its_brand_redirect(self):
        for path, page in self.pages.items():
            with self.subTest(page=str(path.relative_to(SITE))):
                self.assertTrue(any(re.fullmatch(r"0\s*;\s*url\s*=\s*" + re.escape(BRAND), value, re.I)
                                    for value in page.redirects))

    def test_published_javascript_has_no_jquery_below_3_5_0(self):
        outdated = []
        for path in SITE.rglob("*.js"):
            for match in JQUERY_VERSION.finditer(path.read_text(errors="replace")):
                if tuple(map(int, match.groups())) < (3, 5, 0):
                    outdated.append(f"{path.relative_to(SITE)}: {'.'.join(match.groups())}")
        self.assertEqual(outdated, [], "Outdated jQuery is still published: " + ", ".join(outdated))

    def test_local_script_references_resolve(self):
        for path, page in self.pages.items():
            for source in page.scripts:
                url = urlsplit(source)
                if url.scheme or url.netloc:
                    continue
                script = SITE / unquote(url.path).lstrip("/") if url.path.startswith("/") else path.parent / unquote(url.path)
                with self.subTest(page=str(path.relative_to(SITE)), script=source):
                    self.assertTrue(script.is_file(), "A page references a missing script.")

    def test_reported_jquery_url_returns_404(self):
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass

        handler = functools.partial(QuietHandler, directory=str(SITE))
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/assets/js/vendor/jquery-1.7.2.min.js"
            with self.assertRaises(HTTPError) as response:
                with urlopen(url, timeout=5) as asset:
                    asset.read(1)
            with response.exception as error:
                self.assertEqual(error.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
