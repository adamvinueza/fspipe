from fsspec import AbstractFileSystem  # type: ignore
from fsspec.implementations.local import LocalFileSystem  # type: ignore
from typing import Callable, Optional


class Pipe(object):
    """A container for piping data through transformations.

    Args:
        src_fs (AbstractFileSystem): The source file system.
        dest_fs (AbstractFileSystem): The destination file system.
    """
    src_fs: AbstractFileSystem
    dest_fs: AbstractFileSystem

    min_s3_block_size = 5242880

    @staticmethod
    def _get_block_size(buffer_size, fs, filepath):
        """Instead of checking for an S3 file system, just be mindful of the S3
        minimum block size.
        """
        if buffer_size < 0:
            # block size is the file size unless min block size is bigger
            file_size = fs.size(filepath)
            block_size = max(file_size, Pipe.min_s3_block_size)
        else:
            # block size is buffer size unless min block size is bigger
            block_size = max(buffer_size, Pipe.min_s3_block_size)
        return block_size

    def __init__(self, src_fs: Optional[AbstractFileSystem] = None,
                 dest_fs: Optional[AbstractFileSystem] = None):
        if src_fs is None and dest_fs is None:
            src_fs = dest_fs = LocalFileSystem()
        elif bool(src_fs is None) != bool(dest_fs is None):
            if src_fs is None:
                raise ValueError("src_fs is empty")
            if dest_fs is None:
                raise ValueError("dest_fs is empty")
        self.src_fs = src_fs
        self.dest_fs = dest_fs

    def copy(self, src: str, dest: str, readmode: str = 'rb',
             writemode: str = 'wb', bufsize: int = -1) -> None:
        """Copies src to dest.

        Both src and dest paths must be valid in the respective file systems.
        """
        block_size = Pipe._get_block_size(bufsize, self.src_fs, src)
        with self.src_fs.open(src, readmode, block_size) as rdr:
            with self.dest_fs.open(dest, writemode, block_size) as wr:
                wr.write(rdr.read())

    def fcopy(self, src: str, dest: str, fltr: Callable, readmode: str = 'rb',
              writemode: str = 'wb', bufsize: int = -1, **kwargs) -> None:
        """Copies src to dest, passing read bytes through a filter.

        The filter takes a sequence of bytes and whatever keyword arguments are
        passed in, and returns a sequence of bytes.

        Both src and dest paths must be valid in the respective file systems.
        """
        block_size = Pipe._get_block_size(bufsize, self.src_fs, src)
        with self.src_fs.open(src, readmode, block_size) as rdr:
            with self.dest_fs.open(dest, writemode, block_size) as wr:
                while True:
                    b = rdr.read(bufsize)
                    if not b:
                        wr.flush()
                        break
                    wr.write(fltr(b, **kwargs))
