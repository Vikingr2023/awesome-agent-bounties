import os

def migrate_genesis_utxos():
    if is_migration_already_performed():
        raise ValueError("Genesis migration already performed")

    # Existing code to perform the migration
    #...

def is_migration_already_performed():
    # Check if the migration flag is set
    return os.path.exists(MIGRATION_FLAG_FILE)

MIGRATION_FLAG_FILE = "genesis_migration_flag"

# After successful migration, set the flag
with open(MIGRATION_FLAG_FILE, 'w') as f:
    f.write("Migration completed")