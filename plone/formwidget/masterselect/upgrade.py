def v3(context):
    context.runImportStepFromProfile(
            'profile-plone.formwidget.masterselect:default',
            'jsregistry', run_dependencies=False, purge_old=False)
