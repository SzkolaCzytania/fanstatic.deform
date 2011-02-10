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

class deform_resource(object):
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
        needed_requirements = []
        assert isinstance(ignores, list), "ignores must be a list"
        for (requirement, version) in schema.get_widget_requirements():
            if requirement in ignores:
                continue
            if version == None:
                if requirement == 'jquery':
                    jquery.need()
                elif requirement == 'jqueryui':
                    jqueryui.jqueryui.need()
                    if jqueryui_theme:
                        jqueryui_theme.need()
                elif requirement == 'tinymce':
                    tinymce.need()
                elif requirement == 'jquery.form':
                    jquery_form.need()
                elif requirement == 'jquery.maskedinput':
                    jquery_maskedinput.need()
                elif requirement == 'deform':
                    deform_req.need()
                else:
                    raise AttributeError("Unknown requirements. import them "
                                         "on your own and add them to the "
                                         "ignore list")
            else:
                raise AttributeError("Unknown requirements. import them "
                                     "on your own and add them to the "
                                     "ignore list")
