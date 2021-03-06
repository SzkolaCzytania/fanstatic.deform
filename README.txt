fanstatic.deform
================

`Fanstatic <http://fanstatic.org>`_ Is a library for automatic injection
of static resources into your webpages. While doing so it also takes care of
caching and dependencies.

`Deform <http://docs.repoze.org/deform/>`_ Is a library to generate forms. It
provides some javascript and css files. Not all of them are always needed
so it provides a method to query for the resources to include into your
webpage.

fanstatic.deform is a little library that receives a deform form and tells
Fanstatic which resources to include.

In its simplest form, you use it like that:

    >>> from fanstaticdeform import deform_resource
    >>> len(resourcesFanstaticWillLoad())
    0
    >>> deform_resource.needsFor(deform_form)
    >>> len(resourcesFanstaticWillLoad())
    4

Now all resources will get injected.

If you need JQuery UI, you usually also need some css file. JQuery UI has a lot
of css files to choose from. The default one is ui-lightness. But you can
also choose not to include a theme, or select your own:

    >>> addRequirement(deform_form, 'jqueryui')
    >>> from js.jqueryui import trontastic
    >>> deform_resource.needsFor(deform_form, jqueryui_theme = trontastic)
    >>> len(resourcesFanstaticWillLoad())
    6
    >>> 'trontastic' in str(resourcesFanstaticWillLoad())
    True
    >>> 'lightness' in str(resourcesFanstaticWillLoad())
    False

If you explicitly not want to include a theme, pass None as jqueryui_theme.

If you have created your own widgets with unique requirements, the library
will not know how to handle them out of the box.
Either you register your resources, or you add the requirements to the ignore
list:

    >>> addRequirement(deform_form, 'global_observer')
    >>> deform_resource.needsFor(deform_form, ignores = ['global_observer'])

    >>> addRequirement(deform_form, 'extjs')
    >>> from js.extjs import extjs
    >>> deform_resource.register('extjs', None, extjs.all)
    >>> deform_resource.needsFor(deform_form, ignores = ['global_observer'])
    >>> len(resourcesFanstaticWillLoad())
    10
