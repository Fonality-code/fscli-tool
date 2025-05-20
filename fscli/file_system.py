import os
import shutil
import platform
import datetime
import subprocess
import hashlib
import stat
import time
import re
import sys
from collections import namedtuple
try:
    import ctypes
    import string
except ImportError:
    pass  # Handle gracefully if not available


class FileSystem:
    """
    A class to handle common file system operations without external libraries.
    Enhanced for network forensics with capabilities to analyze partitions,
    filesystem types, and detailed system information.
    """

    def __init__(self):
        """Initialize the FileSystem class."""
        self.current_dir = os.getcwd()
        self.os_type = platform.system().lower()

    def _human_readable_size(self, size, decimal_places=2):
        """
        Convert a size in bytes to a human-readable format.

        Args:
            size (int): Size in bytes
            decimal_places (int): Number of decimal places for rounding

        Returns:
            str: Human-readable size (e.g., '1.23 MB')
        """
        if size == 0:
            return '0 B'
        units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        unit_index = 0
        size = float(size)
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return f"{size:.{decimal_places}f} {units[unit_index]}"

    def create_file(self, path, content=""):
        """
        Create a new file with optional content.

        Args:
            path (str): Path of the file to create
            content (str, optional): Content to write to the file. Defaults to empty string.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error creating file: {e}")
            return False

    def read_file(self, path):
        """
        Read content from a file.

        Args:
            path (str): Path of the file to read

        Returns:
            str: File content or empty string if error occurs
        """
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""

    def delete_file(self, path):
        """
        Delete a file.

        Args:
            path (str): Path of the file to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.isfile(path):
                os.remove(path)
                return True
            else:
                print(f"Error: {path} is not a file")
                return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False

    def create_folder(self, path):
        """
        Create a new folder.

        Args:
            path (str): Path of the folder to create

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(path):
                os.makedirs(path)
                return True
            else:
                print(f"Folder already exists: {path}")
                return False
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False

    def delete_folder(self, path, recursive=False):
        """
        Delete a folder.

        Args:
            path (str): Path of the folder to delete
            recursive (bool): If True, delete folder and all contents

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.isdir(path):
                if recursive:
                    shutil.rmtree(path)
                else:
                    os.rmdir(path)  # Will only work if directory is empty
                return True
            else:
                print(f"Error: {path} is not a directory")
                return False
        except Exception as e:
            print(f"Error deleting folder: {e}")
            return False

    def list_files(self, path=None):
        """
        List all files in a directory.

        Args:
            path (str, optional): Directory path. Defaults to current directory.

        Returns:
            list: List of file names in the directory
        """
        try:
            if path is None:
                path = self.current_dir

            file_list = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    file_list.append(item)
            return file_list
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    def list_folders(self, path=None):
        """
        List all folders in a directory.

        Args:
            path (str, optional): Directory path. Defaults to current directory.

        Returns:
            list: List of folder names in the directory
        """
        try:
            if path is None:
                path = self.current_dir

            folder_list = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    folder_list.append(item)
            return folder_list
        except Exception as e:
            print(f"Error listing folders: {e}")
            return []

    def list_all(self, path=None, include_details=False):
        """
        List all files and folders in a directory with optional details.

        Args:
            path (str, optional): Directory path. Defaults to current directory.
            include_details (bool): If True, include file size, modification time

        Returns:
            list: List of dictionaries with file/folder information
        """
        try:
            if path is None:
                path = self.current_dir

            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)

                if include_details:
                    stats = os.stat(item_path)
                    modified_time = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

                    item_info = {
                        'name': item,
                        'type': 'file' if os.path.isfile(item_path) else 'folder',
                        'size': stats.st_size if os.path.isfile(item_path) else None,
                        'modified': modified_time
                    }
                    items.append(item_info)
                else:
                    items.append({
                        'name': item,
                        'type': 'file' if os.path.isfile(item_path) else 'folder'
                    })

            return items
        except Exception as e:
            print(f"Error listing items: {e}")
            return []

    def get_file_size(self, path):
        """
        Get the size of a file in bytes.

        Args:
            path (str): Path of the file

        Returns:
            int: Size of file in bytes, or -1 if error
        """
        try:
            if os.path.isfile(path):
                return os.path.getsize(path)
            else:
                print(f"Error: {path} is not a file")
                return -1
        except Exception as e:
            print(f"Error getting file size: {e}")
            return -1

    def copy_file(self, source, destination):
        """
        Copy a file from source to destination.

        Args:
            source (str): Source file path
            destination (str): Destination file path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            print(f"Error copying file: {e}")
            return False

    def move_file(self, source, destination):
        """
        Move a file from source to destination.

        Args:
            source (str): Source file path
            destination (str): Destination file path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            shutil.move(source, destination)
            return True
        except Exception as e:
            print(f"Error moving file: {e}")
            return False

    def rename(self, old_path, new_path):
        """
        Rename a file or folder.

        Args:
            old_path (str): Current path
            new_path (str): New path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.rename(old_path, new_path)
            return True
        except Exception as e:
            print(f"Error renaming: {e}")
            return False

    def get_drive_space(self, path=None):
        """
        Get drive space information.

        Args:
            path (str, optional): Path to check. Defaults to current directory.

        Returns:
            dict: Dictionary with total, used, and free space in bytes
        """
        try:
            if path is None:
                path = self.current_dir

            total, used, free = shutil.disk_usage(path)
            return {
                'total': total,
                'total_human': self._human_readable_size(total),
                'used': used,
                'used_human': self._human_readable_size(used),
                'free': free,
                'free_human': self._human_readable_size(free),
                'used_percent': round((used / total) * 100, 2)
            }
        except Exception as e:
            print(f"Error getting drive space: {e}")
            return {}

    def get_disk_partitions(self, all_partitions=False):
        """
        Get detailed information about all disk partitions.

        Args:
            all_partitions (bool): If True, include all partitions, otherwise only physical ones.

        Returns:
            list: List of dictionaries with partition information
        """
        try:
            partitions = []

            if self.os_type == 'windows':
                # Windows-specific approach
                drives = []
                bitmask = ctypes.windll.kernel32.GetLogicalDrives() if 'ctypes' in sys.modules else 0
                for letter in string.ascii_uppercase:
                    if bitmask & 1:
                        drives.append(f"{letter}:")
                    bitmask >>= 1

                for drive in drives:
                    try:
                        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive) if 'ctypes' in sys.modules else 0
                        # 0: Unknown, 1: No root dir, 2: Removable, 3: Fixed, 4: Remote, 5: CDROM, 6: RAMDisk
                        drive_types = {
                            0: "UNKNOWN", 1: "NO_ROOT_DIR", 2: "REMOVABLE",
                            3: "FIXED", 4: "REMOTE", 5: "CDROM", 6: "RAMDISK"
                        }

                        fs_type = ""
                        volume_name = ""

                        # Try to get filesystem type and volume name using WMI or other methods
                        try:
                            vol_info = subprocess.check_output(
                                f"cmd /c vol {drive}",
                                stderr=subprocess.STDOUT,
                                universal_newlines=True
                            )
                            for line in vol_info.splitlines():
                                if "Volume in drive" in line and "is" in line:
                                    volume_name = line.split("is")[1].strip()
                        except:
                            pass

                        # Get filesystem type
                        try:
                            fs_info = subprocess.check_output(
                                ["fsutil", "fsinfo", "volumeinfo", drive],
                                stderr=subprocess.STDOUT,
                                universal_newlines=True
                            )
                            for line in fs_info.splitlines():
                                if "File System Name" in line:
                                    fs_type = line.split(":")[1].strip()
                        except:
                            pass

                        # Get space information
                        space_info = self.get_drive_space(drive)

                        part_info = {
                            'device': drive,
                            'mountpoint': drive,
                            'fstype': fs_type,
                            'opts': '',
                            'drive_type': drive_types.get(drive_type, "UNKNOWN"),
                            'volume_name': volume_name,
                            'total_space': space_info.get('total', 0),
                            'free_space': space_info.get('free', 0),
                            'used_space': space_info.get('used', 0),
                            'used_percent': space_info.get('used_percent', 0)
                        }
                        partitions.append(part_info)
                    except Exception as e:
                        print(f"Error getting info for drive {drive}: {e}")
            else:
                # Unix-like systems (Linux, macOS)
                try:
                    mount_output = subprocess.check_output(
                        ['mount'], stderr=subprocess.STDOUT, universal_newlines=True
                    )

                    for line in mount_output.splitlines():
                        parts = line.split()
                        if len(parts) >= 5:
                            device = parts[0]
                            mountpoint = parts[2]
                            fstype = parts[4]
                            opts = parts[5].strip('()')

                            # Skip non-physical devices if requested
                            if not all_partitions and (
                                fstype in ('proc', 'sysfs', 'devpts', 'devtmpfs', 'tmpfs') or
                                device.startswith(('none', '/dev/loop', 'udev'))
                            ):
                                continue

                            # Get space information
                            try:
                                space_info = self.get_drive_space(mountpoint)

                                part_info = {
                                    'device': device,
                                    'mountpoint': mountpoint,
                                    'fstype': fstype,
                                    'opts': opts,
                                    'total_space': space_info.get('total', 0),
                                    'free_space': space_info.get('free', 0),
                                    'used_space': space_info.get('used', 0),
                                    'used_percent': space_info.get('used_percent', 0)
                                }
                                partitions.append(part_info)
                            except Exception as e:
                                print(f"Error getting space info for {mountpoint}: {e}")
                except Exception as e:
                    print(f"Error getting mount information: {e}")

            return partitions
        except Exception as e:
            print(f"Error getting disk partitions: {e}")
            return []

    def get_filesystem_stats(self, path=None):
        """
        Get detailed filesystem statistics for forensic analysis.

        Args:
            path (str, optional): Path to check. Defaults to current directory.

        Returns:
            dict: Dictionary with filesystem statistics
        """
        if path is None:
            path = self.current_dir

        try:
            # Get basic file system stats
            stats = os.statvfs(path) if hasattr(os, 'statvfs') else None

            if stats:
                # Calculate block sizes and counts
                fragment_size = stats.f_frsize or stats.f_bsize
                total_blocks = stats.f_blocks
                free_blocks = stats.f_bfree
                avail_blocks = stats.f_bavail  # Available to non-superuser

                total_inodes = stats.f_files
                free_inodes = stats.f_ffree
                avail_inodes = stats.f_favail  # Available to non-superuser

                # Calculate sizes
                total_size = total_blocks * fragment_size
                free_size = free_blocks * fragment_size
                avail_size = avail_blocks * fragment_size

                # Inode usage
                used_inodes = total_inodes - free_inodes
                inode_usage_percent = (used_inodes / total_inodes * 100) if total_inodes > 0 else 0

                return {
                    'path': os.path.abspath(path),
                    'filesystem_stats': {
                        'block_size': stats.f_bsize,
                        'fragment_size': fragment_size,
                        'total_blocks': total_blocks,
                        'free_blocks': free_blocks,
                        'available_blocks': avail_blocks,
                        'total_inodes': total_inodes,
                        'free_inodes': free_inodes,
                        'available_inodes': avail_inodes,
                        'filesystem_id': stats.f_fsid,
                        'mount_flags': stats.f_flag,
                        'maximum_filename_length': stats.f_namemax
                    },
                    'space_usage': {
                        'total_size': total_size,
                        'total_size_human': self._human_readable_size(total_size),
                        'free_size': free_size,
                        'free_size_human': self._human_readable_size(free_size),
                        'available_size': avail_size,
                        'available_size_human': self._human_readable_size(avail_size),
                        'used_size': total_size - free_size,
                        'used_size_human': self._human_readable_size(total_size - free_size),
                        'usage_percent': ((total_size - free_size) / total_size * 100) if total_size > 0 else 0
                    },
                    'inode_usage': {
                        'used_inodes': used_inodes,
                        'usage_percent': inode_usage_percent
                    }
                }
            else:
                # Fallback for Windows or other systems without statvfs
                space_info = self.get_drive_space(path)

                return {
                    'path': os.path.abspath(path),
                    'space_usage': space_info
                }
        except Exception as e:
            print(f"Error getting filesystem stats: {e}")
            return {}

    def get_current_directory(self):
        """
        Get the current working directory.

        Returns:
            str: Current working directory path
        """
        return os.getcwd()

    def change_directory(self, path):
        """
        Change the current working directory.

        Args:
            path (str): New directory path

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            os.chdir(path)
            self.current_dir = os.getcwd()  # Update the current directory
            return True
        except Exception as e:
            print(f"Error changing directory: {e}")
            return False

    def get_file_hash(self, path, hash_type='md5'):
        """
        Calculate the hash value of a file.

        Args:
            path (str): Path to the file
            hash_type (str): Hash algorithm to use ('md5', 'sha1', 'sha256')

        Returns:
            str: Hash value as hexadecimal string or empty if error
        """
        try:
            if not os.path.isfile(path):
                print(f"Error: {path} is not a file")
                return ""

            hash_funcs = {
                'md5': hashlib.md5,
                'sha1': hashlib.sha1,
                'sha256': hashlib.sha256
            }

            if hash_type not in hash_funcs:
                print(f"Error: Unsupported hash type '{hash_type}'")
                return ""

            hash_obj = hash_funcs[hash_type]()

            with open(path, 'rb') as f:
                # Read file in chunks to handle large files
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_obj.update(chunk)

            return hash_obj.hexdigest()
        except Exception as e:
            print(f"Error calculating file hash: {e}")
            return ""

    def get_file_permissions(self, path):
        """
        Get detailed file permissions in both octal and symbolic format.

        Args:
            path (str): Path to the file or directory

        Returns:
            dict: Dictionary containing permission details
        """
        try:
            if not os.path.exists(path):
                print(f"Error: {path} does not exist")
                return {}

            # Get file stats
            st = os.stat(path)

            # Octal permissions (e.g., 0o755)
            mode = st.st_mode
            octal_perm = oct(mode & 0o777)

            # Symbolic permissions (e.g., rwxr-xr-x)
            symbolic = ''

            # File type prefix
            if stat.S_ISDIR(mode):
                symbolic += 'd'
            elif stat.S_ISLNK(mode):
                symbolic += 'l'
            else:
                symbolic += '-'

            # User permissions
            symbolic += 'r' if mode & stat.S_IRUSR else '-'
            symbolic += 'w' if mode & stat.S_IWUSR else '-'
            symbolic += 'x' if mode & stat.S_IXUSR else '-'

            # Group permissions
            symbolic += 'r' if mode & stat.S_IRGRP else '-'
            symbolic += 'w' if mode & stat.S_IWGRP else '-'
            symbolic += 'x' if mode & stat.S_IXGRP else '-'

            # Other permissions
            symbolic += 'r' if mode & stat.S_IROTH else '-'
            symbolic += 'w' if mode & stat.S_IWOTH else '-'
            symbolic += 'x' if mode & stat.S_IXOTH else '-'

            # Additional attributes
            special_bits = {
                'setuid': bool(mode & stat.S_ISUID),
                'setgid': bool(mode & stat.S_ISGID),
                'sticky': bool(mode & stat.S_ISVTX)
            }

            return {
                'path': os.path.abspath(path),
                'octal': octal_perm,
                'symbolic': symbolic,
                'special_bits': special_bits,
                'owner_id': st.st_uid,
                'group_id': st.st_gid
            }
        except Exception as e:
            print(f"Error getting file permissions: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    fs = FileSystem()

    # Create a test file
    fs.create_file("test.txt", "Hello, this is a test file!")

    # Read the file content
    content = fs.read_file("test.txt")
    print(f"File content: {content}")

    # Get file information
    file_info = fs.list_all(path=".", include_details=True)
    print(f"File info: {file_info}")

    # Create a folder
    fs.create_folder("test_folder")

    # List files and folders
    print(f"Files in current directory: {fs.list_files()}")
    print(f"Folders in current directory: {fs.list_folders()}")

    # Check drive space
    space_info = fs.get_drive_space()
    print(f"Drive space: {space_info}")

    # Clean up (delete test file and folder)
    fs.delete_file("test.txt")
    fs.delete_folder("test_folder")
