import os
import shutil
import datetime
import logging
import json
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config():
    """Load configuration from JSON file"""
    base_dir = Path(__file__).parent
    src_dir = base_dir.parent.parent
    config_file = src_dir / "data" / "config" / "backup_tool.json"

    if not config_file.exists():
        logging.error(
            "⚠️ Configurazione non trovata!"
        )  # Keeping consistent with other apps
        logging.error(f"   Configura l'app nel launcher prima: {config_file}")
        return None

    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        logging.info("✅ Configurazione caricata con successo")
        return config
    except Exception as e:
        logging.error(f"Errore nel caricamento della configurazione: {e}")
        return None


def should_include_file(filename, allowed_extensions):
    """Check if file should be included based on extension"""
    if not allowed_extensions or "*" in allowed_extensions:
        return True

    # Normalize extensions: ensure they start with . and are lowercase
    normalized_exts = [
        (
            ext.strip().lower()
            if ext.strip().startswith(".")
            else f".{ext.strip().lower()}"  # Ensure extension starts with .
        )
        for ext in allowed_extensions
    ]

    return any(filename.lower().endswith(ext) for ext in normalized_exts)


def perform_backup(source_dir, backup_dest_dir, allowed_extensions):
    """Execute the backup copy process"""
    items = os.listdir(source_dir)
    count = 0
    skipped_count = 0

    print(f"\n🚀 Starting backup of {len(items)} items...\n")
    if allowed_extensions and "*" not in allowed_extensions:
        print(f"   Filtering extensions: {allowed_extensions}")

    for item in items:
        # Skip if somehow we are backing up into the source folder
        if os.path.normpath(os.path.join(source_dir, item)) == os.path.normpath(
            backup_dest_dir
        ):
            continue

        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(backup_dest_dir, item)

        try:
            if os.path.isfile(source_path):
                if should_include_file(item, allowed_extensions):
                    shutil.copy2(source_path, dest_path)
                    count += 1
                    print(f"  ✓ File: {item}")
                else:
                    skipped_count += 1
            elif os.path.isdir(source_path):
                # Recursive backup for directories?
                # For now, we copy the tree, but ideally we should filter inside too.
                # simple copytree copies everything.
                # To support filtering inside dirs, we'd need a custom copytree.
                # For simplicity in this version, let's copy directories as is
                # OR skip them if user only wants specific files.
                # Let's keep logic: if it's a dir, we copy it fully for safety
                # (user might lose nested files otherwise).
                shutil.copytree(source_path, dest_path)
                count += 1
                print(f"  ✓ Folder: {item}")
        except Exception as e:
            logging.error(f"Failed to copy '{item}': {e}")

    return count, skipped_count


def get_backup_config():
    """Load and parse backup configuration"""
    config = load_config()
    if not config:
        logging.error("❌ Cannot proceed without configuration.")
        return None, None, None

    source_dir = config.get("source_dir", "")
    dest_dir_base = config.get("dest_dir", "")
    include_extensions_config = config.get(
        "include_extensions", ["*"]
    )  # Default is list ["*"]

    # Handle both list (new) and string (legacy/direct edit) formats
    allowed_extensions = []

    if isinstance(include_extensions_config, str):
        # Handle string input "ext1, ext2"
        if include_extensions_config.strip() != "*":
            allowed_extensions = [
                e.strip() for e in include_extensions_config.split(",")
            ]
    elif isinstance(include_extensions_config, list):
        # Handle list input from multiselect
        # If "*" is in the list, we allow all
        if "*" in include_extensions_config:
            allowed_extensions = []  # Empty means all
        else:
            # Flatten the extensions from keys like ".pdf, .docx"
            for item in include_extensions_config:
                if "," in item:
                    allowed_extensions.extend([e.strip() for e in item.split(",")])
                else:
                    allowed_extensions.append(item.strip())

    # Clean up allowed extensions
    allowed_extensions = [e for e in allowed_extensions if e]

    # Validate config
    if not source_dir or not dest_dir_base:
        logging.error("❌ Configuration incomplete!")
        logging.error(
            "   Please configure Source and Destination folders in the launcher."
        )
        return None, None, None

    return source_dir, dest_dir_base, allowed_extensions


def main():
    logging.info("Starting Backup Tool...")

    source_dir, dest_dir_base, allowed_extensions = get_backup_config()

    if not source_dir:
        input("Press Enter to exit...")
        return

    if not os.path.exists(source_dir):
        logging.error(f"❌ Source folder does not exist: {source_dir}")
        input("Press Enter to exit...")
        return

    # Construct destination
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    source_name = os.path.basename(os.path.normpath(source_dir))
    backup_dest_dir = os.path.join(dest_dir_base, f"backup_{source_name}", timestamp)

    logging.info(f"📁 Source: {source_dir}")
    logging.info(f"📂 Destination: {backup_dest_dir}")

    # Create destination directory
    try:
        os.makedirs(backup_dest_dir, exist_ok=True)
    except OSError as e:
        logging.error(f"Error creating backup directory '{backup_dest_dir}': {e}")
        input("Press Enter to exit...")
        return

    # Run backup
    count, skipped = perform_backup(source_dir, backup_dest_dir, allowed_extensions)

    print("\n" + "=" * 50)
    logging.info(f"✅ Backup completed! {count} items copied.")
    if skipped > 0:
        logging.info(f"ℹ️  Skipped {skipped} files (extension filter).")
    print("=" * 50)

    # Auto close
    import time

    time.sleep(5)


if __name__ == "__main__":
    main()
