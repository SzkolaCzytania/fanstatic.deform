from js.jquery import jquery
from js.jqueryui import trontastic
from js.extjs import extjs
import colander
import deform
import doctest
import fanstatic
import unittest

from fanstaticdeform import deform_resource

HEAVY_FORM_RESOURCES = "[<Resource 'themes/ui-lightness/jquery-ui.css' in library 'jqueryui'>, <Resource 'form.css' in library 'deform'>, <Resource 'jquery.js' in library 'jquery'>, <Resource 'ui/jquery-ui.js' in library 'jqueryui'>, <Resource 'jquery.form.js' in library 'deform'>, <Resource 'deform.js' in library 'deform'>, <Resource 'jquery.maskedinput-1.2.2.min.js' in library 'deform'>, <Resource 'tiny_mce_src.js' in library 'tinymce'>]"
MINIMAL_FORM_RESOURCES = "[<Resource 'form.css' in library 'deform'>, <Resource 'jquery.js' in library 'jquery'>, <Resource 'jquery.form.js' in library 'deform'>, <Resource 'deform.js' in library 'deform'>]"

class Unittests(unittest.TestCase):

    def setUp(self):
        fanstatic.init_needed()

    def getHeavyForm(self):
        schema = colander.Schema()
        form = deform.Form(schema)
        req_registry = form.resource_registry.registry
        all_requirements = []
        for req_key, req_dict in req_registry.items():
            for version in req_dict.keys():
                all_requirements.append((req_key, version))

        form.widget.requirements = all_requirements
        return form

    def testBasicSupport(self):
        deform_resource.needsFor(self.getHeavyForm())

        self.assertEquals(HEAVY_FORM_RESOURCES,
                          str(fanstatic.get_needed().resources()))

    def testDontDoToMuch(self):
        schema = colander.Schema()
        form = deform.Form(schema)

        deform_resource.needsFor(form)

        self.assertEquals(MINIMAL_FORM_RESOURCES,\
                          str(fanstatic.get_needed().resources()))

    def testEnsureWeDontLoadJqueryTwice(self):
        jquery.need()
        deform_resource.needsFor(self.getHeavyForm())

        self.assertEquals(HEAVY_FORM_RESOURCES,\
                          str(fanstatic.get_needed().resources()))

    def testDontSilentlyIgnoreUnknownRequirements(self):
        form = self.getHeavyForm()
        form.widget.requirements.append(('Bogus', None))
        self.assertRaises(AttributeError, deform_resource.needsFor, form)

    def testIgnoreRequirements(self):
        form = self.getHeavyForm()
        form.widget.requirements.append(('Bogus', None))
        deform_resource.needsFor(form, ignores=['Bogus'])
        self.assertEquals(HEAVY_FORM_RESOURCES,\
                          str(fanstatic.get_needed().resources()))

    def testDifferentTheme(self):
        form = self.getHeavyForm()
        deform_resource.needsFor(form, jqueryui_theme = trontastic)
        self.assertTrue('trontastic' in\
                          str(fanstatic.get_needed().resources()))

    def testDifferentThemeNotLoadedIfNotNeeded(self):
        schema = colander.Schema()
        form = deform.Form(schema)

        deform_resource.needsFor(form, jqueryui_theme = trontastic)
        self.assertFalse('trontastic' in\
                          str(fanstatic.get_needed().resources()))

    def testRequirementRegistration(self):
        required_resource = extjs.all
        deform_resource.register('extjs', None, required_resource)
        form = self.getHeavyForm()
        form.widget.requirements.append(('extjs', None))
        deform_resource.needsFor(form)
        self.assertEquals(11, len(fanstatic.get_needed().resources()))

deform_form = deform.Form(colander.Schema())
deform_form.widget.requirements = list(deform_form.widget.requirements)
Tests = unittest.TestSuite()
Tests.addTests(doctest.DocFileSuite('../README.txt', globs={
    "ignore":fanstatic.init_needed(),
    "resourcesFanstaticWillLoad": lambda:fanstatic.get_needed().resources(),
    "addRequirement":lambda form, req:form.widget.requirements.append((req, None)),
    "deform_form" : deform_form,
    }))
Tests.addTests(unittest.TestLoader().loadTestsFromTestCase(Unittests))

