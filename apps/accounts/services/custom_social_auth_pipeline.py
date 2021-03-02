def custom_create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS'))
    if not fields:
        return
    fields['is_valid'] = True
    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


def custom_user_details(strategy, details, backend, user=None, *args, **kwargs):
    if not user:
        return
    changed = False  # flag to track changes
    if strategy.setting('NO_DEFAULT_PROTECTED_USER_FIELDS') is True:
        protected = ()
    else:
        protected = ('username', 'id', 'pk', 'email', 'password',
                     'is_active', 'is_staff', 'is_superuser',)

    protected = protected + tuple(strategy.setting('PROTECTED_USER_FIELDS', []))
    if user.name:
        protected = protected + tuple(['name'])
    print(protected)
    field_mapping = strategy.setting('USER_FIELD_MAPPING', {}, backend)
    for name, value in details.items():

        name = field_mapping.get(name, name)
        if value is None or not hasattr(user, name) or name in protected:
            continue
        current_value = getattr(user, name, None)
        if current_value == value:
            continue
        changed = True
        setattr(user, name, value)
    if changed:
        strategy.storage.user.changed(user)
