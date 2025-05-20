import argparse
import sys
from file_system import FileSystem
from pretty_print import PrettyPrinter

def main():
    """
    Command-line interface for filesystem operations and forensic analysis.
    """
    parser = argparse.ArgumentParser(
        description="Filesystem CLI Tool for Operations and Forensic Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--output",
        help="Output file for logging results",
        default=None
    )
    parser.add_argument(
        "--path",
        help="Path to operate on (default: current directory)",
        default=None
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    parser_list = subparsers.add_parser("list", help="List files and folders")
    parser_list.add_argument(
        "--detailed",
        action="store_true",
        help="Include detailed information (size, modified time)"
    )

    # Space command
    subparsers.add_parser("space", help="Show drive space information")

    # Partitions command
    parser_partitions = subparsers.add_parser("partitions", help="Show disk partition information")
    parser_partitions.add_argument(
        "--all",
        action="store_true",
        help="Include all partitions, including virtual ones"
    )

    # Stats command
    subparsers.add_parser("stats", help="Show filesystem statistics")

    # Permissions command
    parser_perms = subparsers.add_parser("perms", help="Show file or folder permissions")
    parser_perms.add_argument(
        "target",
        help="File or folder to check permissions for"
    )

    # Hash command
    parser_hash = subparsers.add_parser("hash", help="Calculate file hash")
    parser_hash.add_argument(
        "file",
        help="File to calculate hash for"
    )
    parser_hash.add_argument(
        "--type",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm to use (default: sha256)"
    )

    # Create file command
    parser_create_file = subparsers.add_parser("create-file", help="Create a new file")
    parser_create_file.add_argument(
        "file",
        help="Path of the file to create"
    )
    parser_create_file.add_argument(
        "--content",
        default="",
        help="Content to write to the file (default: empty)"
    )

    # Create folder command
    parser_create_folder = subparsers.add_parser("create-folder", help="Create a new folder")
    parser_create_folder.add_argument(
        "folder",
        help="Path of the folder to create"
    )

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a file or folder")
    parser_delete.add_argument(
        "path",
        help="Path of the file or folder to delete"
    )
    parser_delete.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively delete folder and its contents"
    )

    # Copy command
    parser_copy = subparsers.add_parser("copy", help="Copy a file")
    parser_copy.add_argument(
        "source",
        help="Source file path"
    )
    parser_copy.add_argument(
        "destination",
        help="Destination file path"
    )

    # Move command
    parser_move = subparsers.add_parser("move", help="Move a file")
    parser_move.add_argument(
        "source",
        help="Source file path"
    )
    parser_move.add_argument(
        "destination",
        help="Destination file path"
    )

    # Rename command
    parser_rename = subparsers.add_parser("rename", help="Rename a file or folder")
    parser_rename.add_argument(
        "old_path",
        help="Current path"
    )
    parser_rename.add_argument(
        "new_path",
        help="New path"
    )

    # Change directory command
    parser_cd = subparsers.add_parser("cd", help="Change current directory")
    parser_cd.add_argument(
        "path",
        help="New directory path"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    fs = FileSystem()
    printer = PrettyPrinter(output_file=args.output)

    if args.command == "list":
        items = fs.list_all(path=args.path, include_details=args.detailed)
        printer.print_list("Directory Listing", items, detailed=args.detailed)
    elif args.command == "space":
        space_info = fs.get_drive_space(path=args.path)
        printer.print_drive_space("Drive Space Information", space_info)
    elif args.command == "partitions":
        partitions = fs.get_disk_partitions(all_partitions=args.all)
        printer.print_partitions("Disk Partitions", partitions)
    elif args.command == "stats":
        stats = fs.get_filesystem_stats(path=args.path)
        printer.print_filesystem_stats("Filesystem Statistics", stats)
    elif args.command == "perms":
        perms = fs.get_file_permissions(args.target)
        printer.print_file_permissions(f"Permissions for {args.target}", perms)
    elif args.command == "hash":
        hash_value = fs.get_file_hash(args.file, hash_type=args.type)
        printer.print_file_hash(f"Hash for {args.file}", hash_value, args.type)
    elif args.command == "create-file":
        success = fs.create_file(args.file, content=args.content)
        print(f"File creation {'successful' if success else 'failed'}: {args.file}")
    elif args.command == "create-folder":
        success = fs.create_folder(args.folder)
        print(f"Folder creation {'successful' if success else 'failed'}: {args.folder}")
    elif args.command == "delete":
        if fs.delete_file(args.path) or fs.delete_folder(args.path, recursive=args.recursive):
            print(f"Deletion successful: {args.path}")
        else:
            print(f"Deletion failed: {args.path}")
    elif args.command == "copy":
        success = fs.copy_file(args.source, args.destination)
        print(f"File copy {'successful' if success else 'failed'}: {args.source} to {args.destination}")
    elif args.command == "move":
        success = fs.move_file(args.source, args.destination)
        print(f"File move {'successful' if success else 'failed'}: {args.source} to {args.destination}")
    elif args.command == "rename":
        success = fs.rename(args.old_path, args.new_path)
        print(f"Rename {'successful' if success else 'failed'}: {args.old_path} to {args.new_path}")
    elif args.command == "cd":
        success = fs.change_directory(args.path)
        print(f"Directory change {'successful' if success else 'failed'}: {args.path}")

if __name__ == "__main__":
    main()
