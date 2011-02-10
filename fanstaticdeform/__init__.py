from fanstatic import Library, Resource, GroupResource
from js import jqueryui
from js.jquery import jquery
from js.tinymce import tinymce

deform_library = Library('deform', 'deform_resources')

jquery_form = Resource(deform_library, 'jquery.form.js',
                       depends=[jquery])

jquery_maskedinput = Resource(deform_library,\
                              'jquery.maskedinput-1.2.2.min.js',\
                              depends=[jquery])

deform_req = GroupResource([
        Resource(deform_library, 'form.css'),
        Resource(deform_library, 'theme.css'),
        Resource(deform_library, 'deform.js', depends=[jquery, jquery_form])
                           ])
def getDefaultRegistry():
    return {
        'jquery' : {None : set([jquery])},
        'jqueryui' : {None : set([jqueryui.jqueryui])},
        'tinymce' : {None : set([tinymce])},
        'jquery.form' : {None : set([jquery_form])},
        'jquery.maskedinput' : {None : set([jquery_maskedinput])},
        'deform' : {None : set([deform_req])},
    }

class deform_resource(object):
    registry = getDefaultRegistry()
    @classmethod
    def needsFor(cls, schema, ignores = [], jqueryui_theme = jqueryui.ui_lightness):
        """
        Try to "need" every resource required for the given schema
        If the ignore list is not empty, ignore all requirements
        on the list.
        If you have a requirement that you cannot meet and that
        is not on the ignores list, raise an AttributeError
        If jqueryui_theme is required, automatically load
        the jqueryui_theme ui_lightness, or the one provided
        with the argument jqueryui_theme
        Do not load a theme, if jqueryui_theme is set to None or ''
        """
        assert isinstance(ignores, list), "ignores must be a list"
        for (requirement, version) in schema.get_widget_requirements():
            if requirement == 'jqueryui':
                if jqueryui_theme:
                    jqueryui_theme.need()
            if requirement in ignores:
                continue
            requirements = cls.registry.get(requirement, {}).get(version, None)
            if requirements is None:
                raise AttributeError("Unknown requirements. import them "
                                     "on your own and add them to the "
                                     "ignore list or register them via "
                                     "deform_resource.register")
            else:
                for requirement in requirements:
                    requirement.need()

    @classmethod
    def register(cls, requirement, version, resource):
        """
        Register a fanstatic.Resource resource under the requirement requirement
        for the version version.
        """
        assert hasattr(resource, 'need') and callable(resource.need), ""+\
            "You must register objects that are resource like"
        if requirement not in cls.registry:
            cls.registry[requirement] = {}
        if version not in cls.registry:
            cls.registry[requirement][version] = set()
        cls.registry[requirement][version].add(resource)
