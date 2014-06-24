Changelog
=========

1.4 (unreleased)
----------------

- Move to plone.app.testing. Migrate selenium tests from windmill to
  robotframework.
  [saily]

- Add travis and coveralls integration.
  [saily]

- Documentation updates. Fix rst error in ``CHANGES.rst``. Add an example
  to ``README.rst``.
  [saily]

- Add egg-contained buildout.
  [saily]


1.3 (2014-06-16)
----------------

- Do not use fast transition on initial trigger.
  [thomasdesvenain]

- Master select features work when form is loaded in an overlay.
  [thomasdesvenain]

- Fix bug when masterselect is in a fieldset that is not visible.
  [cedricmessiant]

- Add master select radio widget and ability to specify a master Selector
  instead of masterID [ebrehault]


1.2 (2013-11-04)
----------------

- Added a ('fast') jQuery transition on show/hide function.
  [thomasdesvenain]


1.1 (2013-08-26)
----------------

- Made compatible with z3c.form 3.0 and jQuery 1.6+.
  Note: this version drops compatibility with jQuery 1.4.
  Please use plone.formwidget.masterselect 1.0 for plone
  versions < 4.3


1.0 (2013-06-10)
----------------

- Replaced jq by jQuery in generated scripts.
  [vincentfretin]

- Removed plone.directives.form dependency
  Removed plone.app.jquerytools dependency
  Fixed demo profile
  Made some cleanup
  [cedricmessiant]

- Initial checkin, ready for testing.
  [JMehring]
