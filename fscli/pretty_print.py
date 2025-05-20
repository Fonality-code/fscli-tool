import sys
from datetime import datetime
from typing import List, Dict, Any

class PrettyPrinter:
    """
    A class to handle formatted printing of filesystem information.
    Provides customizable output for console and file logging.
    """

    def __init__(self, output_file: str = None, width: int = 80):
        """
        Initialize the PrettyPrinter class.

        Args:
            output_file (str, optional): Path to file for logging output.
            width (int): Maximum line width for formatting output.
        """
        self.output_file = output_file
        self.width = width
        self.border_char = "="
        self.section_char = "-"

    def _write_output(self, text: str) -> None:
        """
        Write text to both console and optional output file.

        Args:
            text (str): Text to output.
        """
        print(text)
        if self.output_file:
            try:
                with open(self.output_file, 'a') as f:
                    f.write(text + '\n')
            except Exception as e:
                print(f"Error writing to output file: {e}")

    def print_header(self, title: str) -> None:
        """
        Print a formatted header with a title.

        Args:
            title (str): Header title.
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        header = f"\n{self.border_char * self.width}\n{title}\nTimestamp: {timestamp}\n{self.border_char * self.width}"
        self._write_output(header)

    def print_list(self, title: str, items: List[Any], detailed: bool = False) -> None:
        """
        Print a formatted list of items (e.g., files or folders).

        Args:
            title (str): Title for the list section.
            items (List[Any]): List of items to print (strings or dictionaries).
            detailed (bool): If True, expect dictionaries with detailed info.
        """
        self.print_header(title)
        if not items:
            self._write_output("No items found.")
            return

        if detailed and isinstance(items[0], dict):
            # Determine column widths for detailed output
            headers = ['Name', 'Type', 'Size', 'Modified']
            max_name = max(len(item['name']) for item in items)
            max_type = max(len(item['type']) for item in items)
            max_size = max(len(self._format_size(item.get('size', 0))) for item in items)
            max_modified = max(len(item.get('modified', '')) for item in items)

            # Print header
            header = (f"{'Name':<{max_name}}  {'Type':<{max_type}}  "
                     f"{'Size':<{max_size}}  {'Modified':<{max_modified}}")
            self._write_output(header)
            self._write_output(self.section_char * self.width)

            # Print items
            for item in items:
                size = self._format_size(item.get('size', 0)) if item.get('size') else 'N/A'
                modified = item.get('modified', 'N/A')
                row = (f"{item['name']:<{max_name}}  {item['type']:<{max_type}}  "
                       f"{size:<{max_size}}  {modified:<{max_modified}}")
                self._write_output(row)
        else:
            # Simple list output
            for item in items:
                self._write_output(str(item))

    def _format_size(self, size: int) -> str:
        """
        Convert size in bytes to human-readable format.

        Args:
            size (int): Size in bytes.

        Returns:
            str: Human-readable size.
        """
        if size == -1 or size is None:
            return 'N/A'
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        size = float(size)
        unit_index = 0
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return f"{size:.2f} {units[unit_index]}"

    def print_drive_space(self, title: str, space_info: Dict[str, Any]) -> None:
        """
        Print formatted drive space information.

        Args:
            title (str): Title for the drive space section.
            space_info (Dict[str, Any]): Dictionary with drive space details.
        """
        self.print_header(title)
        if not space_info:
            self._write_output("No drive space information available.")
            return

        fields = [
            ('Total Space', space_info.get('total_human', 'N/A')),
            ('Used Space', space_info.get('used_human', 'N/A')),
            ('Free Space', space_info.get('free_human', 'N/A')),
            ('Used Percent', f"{space_info.get('used_percent', 0):.2f}%")
        ]

        max_label = max(len(label) for label, _ in fields)
        for label, value in fields:
            self._write_output(f"{label:<{max_label}}: {value}")

    def print_partitions(self, title: str, partitions: List[Dict[str, Any]]) -> None:
        """
        Print formatted disk partition information.

        Args:
            title (str): Title for the partitions section.
            partitions (List[Dict[str, Any]]): List of partition dictionaries.
        """
        self.print_header(title)
        if not partitions:
            self._write_output("No partition information available.")
            return

        headers = ['Device', 'Mountpoint', 'FSType', 'Drive Type', 'Volume Name', 'Used %']
        max_lengths = {h: len(h) for h in headers}
        for part in partitions:
            max_lengths['Device'] = max(max_lengths['Device'], len(part.get('device', '')))
            max_lengths['Mountpoint'] = max(max_lengths['Mountpoint'], len(part.get('mountpoint', '')))
            max_lengths['FSType'] = max(max_lengths['FSType'], len(part.get('fstype', '')))
            max_lengths['Drive Type'] = max(max_lengths['Drive Type'], len(part.get('drive_type', '')))
            max_lengths['Volume Name'] = max(max_lengths['Volume Name'], len(part.get('volume_name', '')))
            max_lengths['Used %'] = max(max_lengths['Used %'], len(f"{part.get('used_percent', 0):.2f}%"))

        # Print header
        header = (f"{'Device':<{max_lengths['Device']}}  "
                  f"{'Mountpoint':<{max_lengths['Mountpoint']}}  "
                  f"{'FSType':<{max_lengths['FSType']}}  "
                  f"{'Drive Type':<{max_lengths['Drive Type']}}  "
                  f"{'Volume Name':<{max_lengths['Volume Name']}}  "
                  f"{'Used %':<{max_lengths['Used %']}}")
        self._write_output(header)
        self._write_output(self.section_char * self.width)

        # Print partitions
        for part in partitions:
            row = (f"{part.get('device', 'N/A'):<{max_lengths['Device']}}  "
                   f"{part.get('mountpoint', 'N/A'):<{max_lengths['Mountpoint']}}  "
                   f"{part.get('fstype', 'N/A'):<{max_lengths['FSType']}}  "
                   f"{part.get('drive_type', 'N/A'):<{max_lengths['Drive Type']}}  "
                   f"{part.get('volume_name', 'N/A'):<{max_lengths['Volume Name']}}  "
                   f"{part.get('used_percent', 0):.2f}%:<{max_lengths['Used %']}")
            self._write_output(row)

    def print_filesystem_stats(self, title: str, stats: Dict[str, Any]) -> None:
        """
        Print formatted filesystem statistics.

        Args:
            title (str): Title for the filesystem stats section.
            stats (Dict[str, Any]): Dictionary with filesystem statistics.
        """
        self.print_header(title)
        if not stats:
            self._write_output("No filesystem statistics available.")
            return

        self._write_output(f"Path: {stats.get('path', 'N/A')}")
        self._write_output(self.section_char * self.width)

        # Space Usage
        if 'space_usage' in stats:
            self._write_output("Space Usage:")
            space = stats['space_usage']
            fields = [
                ('Total Size', space.get('total_size_human', 'N/A')),
                ('Used Size', space.get('used_size_human', 'N/A')),
                ('Free Size', space.get('free_size_human', 'N/A')),
                ('Available Size', space.get('available_size_human', 'N/A')),
                ('Usage Percent', f"{space.get('usage_percent', 0):.2f}%")
            ]
            max_label = max(len(label) for label, _ in fields)
            for label, value in fields:
                self._write_output(f"  {label:<{max_label}}: {value}")

        # Filesystem Stats
        if 'filesystem_stats' in stats:
            self._write_output("\nFilesystem Stats:")
            fs_stats = stats['filesystem_stats']
            fields = [
                ('Block Size', f"{fs_stats.get('block_size', 'N/A')} bytes"),
                ('Fragment Size', f"{fs_stats.get('fragment_size', 'N/A')} bytes"),
                ('Total Blocks', fs_stats.get('total_blocks', 'N/A')),
                ('Free Blocks', fs_stats.get('free_blocks', 'N/A')),
                ('Available Blocks', fs_stats.get('available_blocks', 'N/A')),
                ('Total Inodes', fs_stats.get('total_inodes', 'N/A')),
                ('Free Inodes', fs_stats.get('free_inodes', 'N/A')),
                ('Available Inodes', fs_stats.get('available_inodes', 'N/A')),
                ('Filesystem ID', fs_stats.get('filesystem_id', 'N/A')),
                ('Maximum Filename Length', fs_stats.get('maximum_filename_length', 'N/A'))
            ]
            max_label = max(len(label) for label, _ in fields)
            for label, value in fields:
                self._write_output(f"  {label:<{max_label}}: {value}")

        # Inode Usage
        if 'inode_usage' in stats:
            self._write_output("\nInode Usage:")
            inode = stats['inode_usage']
            fields = [
                ('Used Inodes', inode.get('used_inodes', 'N/A')),
                ('Usage Percent', f"{inode.get('usage_percent', 0):.2f}%")
            ]
            max_label = max(len(label) for label, _ in fields)
            for label, value in fields:
                self._write_output(f"  {label:<{max_label}}: {value}")

    def print_file_permissions(self, title: str, perms: Dict[str, Any]) -> None:
        """
        Print formatted file permission information.

        Args:
            title (str): Title for the permissions section.
            perms (Dict[str, Any]): Dictionary with permission details.
        """
        self.print_header(title)
        if not perms:
            self._write_output("No permission information available.")
            return

        fields = [
            ('Path', perms.get('path', 'N/A')),
            ('Octal Permissions', perms.get('octal', 'N/A')),
            ('Symbolic Permissions', perms.get('symbolic', 'N/A')),
            ('Owner ID', perms.get('owner_id', 'N/A')),
            ('Group ID', perms.get('group_id', 'N/A')),
            ('SetUID', str(perms.get('special_bits', {}).get('setuid', 'N/A'))),
            ('SetGID', str(perms.get('special_bits', {}).get('setgid', 'N/A'))),
            ('Sticky Bit', str(perms.get('special_bits', {}).get('sticky', 'N/A')))
        ]

        max_label = max(len(label) for label, _ in fields)
        for label, value in fields:
            self._write_output(f"{label:<{max_label}}: {value}")

    def print_file_hash(self, title: str, hash_value: str, hash_type: str) -> None:
        """
        Print formatted file hash information.

        Args:
            title (str): Title for the hash section.
            hash_value (str): Calculated hash value.
            hash_type (str): Type of hash (e.g., 'md5', 'sha256').
        """
        self.print_header(title)
        if not hash_value:
            self._write_output("No hash value available.")
            return
        self._write_output(f"{hash_type.upper()} Hash: {hash_value}")



from file_system import FileSystem
from pretty_print import PrettyPrinter

if __name__ == "__main__":
    # Example usage
    fs = FileSystem()
    printer = PrettyPrinter(output_file="filesystem_log.txt")

    # List files with details
    files = fs.list_all(include_details=True)
    printer.print_list("Directory Listing", files, detailed=True)

    # Get and print drive space
    space_info = fs.get_drive_space()
    printer.print_drive_space("Drive Space Information", space_info)

    # Get and print partition information
    partitions = fs.get_disk_partitions()
    printer.print_partitions("Disk Partitions", partitions)

    # Get and print filesystem stats
    stats = fs.get_filesystem_stats()
    printer.print_filesystem_stats("Filesystem Statistics", stats)

    # Get and print file permissions
    perms = fs.get_file_permissions("example.txt")
    printer.print_file_permissions("File Permissions", perms)

    # Get and print file hash
    hash_value = fs.get_file_hash("example.txt", hash_type="sha256")
    printer.print_file_hash("File Hash", hash_value, "sha256")
