from configparser import ConfigParser
from s3fs import S3FileSystem  # type: ignore
from fsspec import AbstractFileSystem  # type: ignore
from fsspec.implementations.local import LocalFileSystem  # type: ignore
from fsspec.implementations.sftp import SFTPFileSystem  # type: ignore
from typing import Optional
import os.path


def S3FS(profile_name: Optional[str] = None) -> AbstractFileSystem:
    if profile_name:
        creds_path = os.path.join(
            os.path.expanduser('~'),
            '.aws/credentials'
        )
        conf = ConfigParser()
        conf.read(creds_path)
        aws_access_key_id = conf.get(profile_name, 'aws_access_key_id'),
        aws_secret_access_key = conf.get(profile_name,
                                         'aws_secret_access_key'),
        aws_session_token = conf.get(profile_name, 'aws_session_token')
        return S3FileSystem(
            anon=False,
            key=aws_access_key_id,
            secret=aws_secret_access_key,
            token=aws_session_token
        )
    # No profile was specified, so use AWS default credentials.
    return S3FileSystem()


def LocalFS() -> AbstractFileSystem:
    return LocalFileSystem()


def SFTPFS(host: str,
           temppath: str,
           username: str,
           password: str,
           port: int) -> AbstractFileSystem:
    return SFTPFileSystem(host,
                          temppath,
                          {
                              'username': username,
                              'password': password,
                              'port': port
                          })
