import sys
import os.path as osp
import unittest
from sphinx_testing import with_app


sphinx_supp = osp.abspath(osp.join(osp.dirname(__file__), 'sphinx_supp'))


sys.path.insert(0, sphinx_supp)


def in_between(full, sub, s0, *others):
    i0 = full.index(s0)
    try:
        last = min(filter(lambda i: i > i0, map(full.index, others)))
    except ValueError:  # empty sequence
        last = len(full)
    return full.index(sub) > i0 and full.index(sub) < last


def get_html(app, fname):
    with open(app.outdir + '/' + fname) as f:
        return f.read()


class TestAutosummaryDocumenter(unittest.TestCase):

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module.html')
        print(html)
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('Should be skipped', html)
        self.assertIn('Should be included', html)

        self.assertNotIn('Should also be skipped', html)
        self.assertIn('Should also be included', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module_no_nesting(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module_no_nesting.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('Should be skipped', html)
        self.assertIn('Should be included', html)

        self.assertNotIn('Should also be skipped', html)
        self.assertIn('Should also be included', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module_summary_only(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module_summary_only.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('<dt id="dummy.Class_CallTest">', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_module_with_title(self, app, status, warning):
        app.build()
        html = get_html(app, 'test_module_title.html')
        self.assertIn('<span class="pre">TestClass</span>', html)
        self.assertIn('<span class="pre">test_func</span>', html)
        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('Should be skipped', html)
        self.assertIn('Should be included', html)

        self.assertNotIn('Should also be skipped', html)
        self.assertIn('Should also be included', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_class(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_class.html')

        self.assertIn('<span class="pre">instance_attribute</span>', html)

        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test escaping of *
        self.assertNotIn(r'\*args', html)
        self.assertNotIn(r', \*\*kwargs', html)
        self.assertIn('*args', html)
        self.assertIn('**kwargs', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)
        self.assertIn('Caller docstring for class attribute', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('Should be skipped', html)
        self.assertIn('Should be included', html)

        self.assertIn('DummySection', html)
        self.assertTrue(in_between(
            html, '<span class="pre">class_caller</span>', 'DummySection',
            'Attributes', 'Methods'),
            msg='class_caller Attribute not in the right Section!')

        # check if the InnerClass is in the Classes section (which ends with
        # the DummySection)
        self.assertTrue(in_between(
            html, '<span class="pre">InnerClass</span>', 'Classes',
            'DummySection'))

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_class_summary_only(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_class_summary_only.html')

        self.assertIn('<span class="pre">instance_attribute</span>', html)

        self.assertIn('<span class="pre">test_method</span>', html)
        self.assertIn('<span class="pre">test_attr</span>', html)

        # test whether the right objects are included
        self.assertIn('<span class="pre">class_caller</span>', html)

        # test whether the data is shown correctly
        self.assertIn('<span class="pre">large_data</span>', html)
        self.assertIn('<span class="pre">small_data</span>', html)

        self.assertNotIn('<dt id="dummy.TestClass.small_data">', html)

    @with_app(buildername='html', srcdir=sphinx_supp,
              copy_srcdir_to_tmpdir=True)
    def test_inherited(self, app, status, warning):
        app.build()
        html = get_html(app, '/test_inherited.html')
        self.assertIn('<span class="pre">test_method</span>', html)


if __name__ == '__main__':
    unittest.main()
