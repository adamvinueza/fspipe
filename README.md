# fspipe 
Library for performing file-to-file transformations, possibly between disparate
file systems.

## Why fspipe?

Userspace file systems are increasingly popular, and with Amazon's S3 becoming a
de facto standard for storing files, the number of ways of interacting with
files is proliferating. The [fsspec]() Python package introduced a standard
Pythonic file-system interface for interacting with disparate userspace file
systems. Its introduction led to new packages for interacting with various
file-system-like interfaces such as S3, GCP and SFTP. 

`fspipe` is a simple `fsspec`-compatible mechanism for transferring files
_between_ file-system-like interfaces. Use `fspipe` to transfer files between S3
buckets, or between SFTP servers and S3 buckets, or between S3 buckets and a
local file system. Or use it to pass files through transformations while moving
them from one file system to another.

## Installation

```
pip install fspipe
```

## Sample usage

Upload a file to S3:
```
from fspipe import Pipe, LocalFS, S3FS

pipe = Pipe(src_fs=LocalFS(), dest_fs=S3FS())
pipe.copy('/path/to/myfile.txt', 's3://my_bucket/myfile.txt')
```

Download a gzipped file from S3 and decompress it to your local file system:
```
from fspipe import Pipe, LocalFS, S3FS
import gzip


pipe = Pipe(src_fs=S3FS(), dest_fs=LocalFS())
src_file = 's3://mybucket/myfile.gz'
dest_file = 'myfile.txt'

# gzip.decompress takes a bytes object and returns a bytes object
pipe.fcopy(src_file, dest_file, gzip.decompress)
```
