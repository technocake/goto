


def migrate_check(magic, command, args, options):

    if not detect_unmigrated_data():
        return "Nothing to migrate", None
    elif '--check-migrate' in command:
        return None, GotoWarning('data_not_migrated')
