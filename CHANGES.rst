Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.4.0 (2020-09-07)
------------------

New features:


- Drop Plone 4.3 support.
  [maurits] (#3130)


Bug fixes:


- Fixed deprecation warning for ComponentLookupError.
  [maurits] (#3130)


1.3.2 (2020-04-20)
------------------

Bug fixes:


- Minor packaging updates. (#1)


1.3.1 (2020-03-08)
------------------

Bug fixes:


- Improved documentation.  [jensens] (#0)


1.3.0 (2019-02-13)
------------------

New features:


- New option ``former_dotted_names`` that allows to register the former name
  under which a behavior used to be registerd. This can be useful to ensure a
  smooth transition in case a behavior's dotted name is changed. [pysailor]
  (#18)


1.2.1 (2018-01-17)
------------------

Bug fixes:

- Fixed import of dotted path in example.  [fulv]


1.2.0 (2017-03-23)
------------------

New features:

- For zcml registration:
  If both, no ``for`` and no ``@adapter`` is given,
  fall first back to ``marker`` if given (new),
  else to ``Interface`` (as it was already before).
  [jensens]

Bug fixes:

- Cleanup: Make Jenkins CI code analysis silent by fixing the issues.
  [jensens]


1.1.4 (2016-12-06)
------------------

Bug fixes:

- Add already introduced attribute ``name`` to interface IBehavior.
  This was missing.
  Also modernized other IBehavior interface descriptions a bit.
  [jensens]


1.1.3 (2016-11-09)
------------------

New features:

- Support Python 3. [davisagli]


1.1.2 (2016-08-11)
------------------

New:

- New option to register a behavior only by it's short name and not by it's dotted name.
  This enables more advanced behavior subclassing capabilities.
  [jensens]


1.1.1 (2016-02-25)
------------------

Fixes:

- Make doctest comparison more robust against zope.component __repr__ changes.
  [thet]


1.1 (2015-07-18)
----------------

- Corrected typo in warning.
  [jensens]

- Add name to behavior directive. This name can be used to lookup behavior
  registrations by new plone.behaviors.registration.
  lookup_behavior_registration function.
  [rnixx]

- Added more documentation, simplified code in directive, added a warning if
  ``for`` is given w/o ``factory``.
  [jensens]


1.0.3 (2015-04-29)
------------------

- Code modernization: utf-header, pep8, rst-files, adapter/implementer
  decorators, ...
  [jensens]


1.0.2 (2013-01-17)
------------------

- Remove dependence of tests on zope.app.testing.
  [davisagli]


1.0.1 - 2011-05-20
------------------

- Relicense under BSD license.
  See http://plone.org/foundation/materials/foundation-resolutions/plone-framework-components-relicensing-policy
  [davisagli]


1.0 - 2011-04-30
----------------

- Use stdlib doctest instead of the deprecated one in zope.testing.
  [davisagli]

- 'plone:behavior' zcml directive use now MessageID for title and description.
  [sylvainb]


1.0b6 - 2009-11-17
------------------

- Fix tests for Zope 2.12
  [optilude]


1.0b5 - 2009-07-12
------------------

- Changed API methods and arguments to mixedCase to be more consistent with
  the rest of Zope. This is a non-backwards-compatible change. Our profuse
  apologies, but it's now or never. :-/

  If you find that you get import errors or unknown keyword arguments in your
  code, please change names from foo_bar too fooBar, e.g.
  enumerate_behaviors() becomes enumerateBehaviors().
  [optilude]


1.0b4 - 2009-06-07
------------------

- Allow a marker-interface-only behavior to be set by using the 'provides'
  attribute (previously 'interface') in the <plone:behavior /> directive
  without a 'factory' attribute. The 'marker' attribute (previously known as
  'subtype') is now only required if there is a marker used in addition to
  a behavior adapter with a separate interface ('provides') and factory.
  [optilude]

- Rename the 'interface' attribute of <plone:behavior /> to 'provides' to
  be more consistent with the <adapter /> directive. This is a backwards
  incompatible change!
  [optilude]

- Rename the 'subtype' attribute of <plone:behavior /> to 'marker' to
  be more explicit about its purpose. This is a backwards
  incompatible change!
  [optilude]


1.0b3 - 2009-04-17
------------------

- Allow behaviors with no factory.
  [alecm]

- Provide a vocabulary of available behaviors.
  [davisagli]


1.0b1 - 2008-04-27
------------------

- Initial release
