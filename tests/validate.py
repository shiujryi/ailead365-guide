"""Dependency-free checks for public static content and Pages portability."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


class PublicSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (ROOT / 'index.html').read_text(encoding='utf-8')
        cls.elements = Document(cls.text).elements
        cls.ids = [attrs['id'] for _, attrs in cls.elements if 'id' in attrs]

    def test_unique_ids_and_local_links(self):
        self.assertEqual(len(self.ids), len(set(self.ids)), 'Duplicate element IDs')
        for tag, attrs in self.elements:
            for key in ('href', 'src'):
                if key not in attrs:
                    continue
                ref = urlsplit(attrs[key])
                if ref.scheme or ref.netloc:
                    continue
                with self.subTest(tag=tag, link=attrs[key]):
                    self.assertFalse(ref.path.startswith('/'), 'Use project-relative paths')
                    if ref.path:
                        target = (ROOT / unquote(ref.path)).resolve()
                        self.assertTrue(target.is_relative_to(ROOT))
                        self.assertTrue(target.is_file(), f'Missing asset: {target}')
                    if ref.fragment and not ref.path:
                        self.assertIn(unquote(ref.fragment), self.ids)

    def test_role_relationships(self):
        tabs = [a for _, a in self.elements if a.get('role') == 'tab']
        panels = [a for _, a in self.elements if a.get('role') == 'tabpanel']
        self.assertEqual(len(tabs), 3)
        self.assertEqual(len(panels), 3)
        for tab in tabs:
            matches = [p for p in panels if p['id'] == tab['aria-controls']]
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0]['aria-labelledby'], tab['id'])
        self.assertEqual(sum(t['aria-selected'] == 'true' for t in tabs), 1)

    def test_external_links_and_login_destination(self):
        logins = []
        for tag, attrs in self.elements:
            if tag != 'a':
                continue
            if attrs.get('target') == '_blank':
                self.assertTrue({'noopener', 'noreferrer'} <= set(attrs.get('rel', '').split()))
            if 'ailead365.com' in attrs.get('href', ''):
                logins.append(attrs['href'])
        self.assertGreaterEqual(len(logins), 3)
        self.assertEqual(set(logins), {'https://csjhkl.ailead365.com/auth/login'})

    def test_no_account_collection(self):
        self.assertFalse(any(tag in {'form', 'input', 'iframe'} for tag, _ in self.elements))
        js = (ROOT / 'assets/app.js').read_text(encoding='utf-8')
        self.assertNotRegex(js, r'\b(localStorage|sessionStorage|fetch|XMLHttpRequest)\b')
        self.assertNotIn('document.cookie', js)
        # Catch accidental inclusion of school-specific fixed-password rules.
        public_text = self.text + js
        self.assertNotRegex(public_text, r'MMDD|生日|身分證|身份證|預設密碼[\s：:為是]*\d{4}')

    def test_public_assets_allowlist(self):
        allowed = {'.css', '.js', '.svg', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.ico', '.woff', '.woff2'}
        assets = list((ROOT / 'assets').rglob('*'))
        self.assertTrue(assets)
        for path in assets:
            if path.is_file():
                self.assertIn(path.suffix.lower(), allowed, f'Unexpected public file: {path}')
                self.assertFalse(path.is_symlink())
        for tag, attrs in self.elements:
            if tag == 'script':
                self.assertTrue(attrs.get('src', '').startswith('./assets/'), 'No remote scripts')


if __name__ == '__main__':
    unittest.main(verbosity=2)
