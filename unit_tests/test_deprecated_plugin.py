import unittest
from nose.config import Config
from nose.plugins.deprecated import Deprecated, DeprecatedTest
from nose.result import TextTestResult
from io import StringIO
from optparse import OptionParser


class TestDeprecatedPlugin(unittest.TestCase):

    def test_api_present(self):
        sk = Deprecated()
        sk.addOptions
        sk.configure
        sk.prepareTestResult                

    def test_deprecated_output(self):
        class TC(unittest.TestCase):
            def test(self):
                raise DeprecatedTest('deprecated me')

        stream = unittest._WritelnDecorator(StringIO())
        res = TextTestResult(stream, 0, 1)
        sk = Deprecated()
        sk.prepareTestResult(res)

        test = TC('test')
        test(res)
        assert not res.errors, "Deprecated was not caught: %s" % res.errors
        assert res.deprecated            

        res.printErrors()
        out = stream.getvalue()
        assert out
        assert out.strip() == "D"
        assert res.wasSuccessful()

    def test_deprecated_output_verbose(self):

        class TC(unittest.TestCase):
            def test(self):
                raise DeprecatedTest('deprecated me too')
        
        stream = unittest._WritelnDecorator(StringIO())
        res = TextTestResult(stream, 0, verbosity=2)
        sk = Deprecated()
        sk.prepareTestResult(res)
        test = TC('test')
        test(res)
        assert not res.errors, "Deprecated was not caught: %s" % res.errors
        assert res.deprecated            

        res.printErrors()
        out = stream.getvalue()
        print(out)
        assert out

        assert ' ... DEPRECATED' in out
        assert 'deprecated me too' in out

    def test_enabled_by_default(self):
        sk = Deprecated()
        assert sk.enabled, "Deprecated was not enabled by default"

    def test_can_be_disabled(self):
        parser = OptionParser()
        sk = Deprecated()
        sk.addOptions(parser)
        options, args = parser.parse_args(['--no-deprecated'])
        sk.configure(options, Config())
        assert not sk.enabled, \
               "Deprecated was not disabled by noDeprecated option"
        

if __name__ == '__main__':
    unittest.main()
