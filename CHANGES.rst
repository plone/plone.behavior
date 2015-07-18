=========
Changelog
=========

1.1 (unreleased)
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