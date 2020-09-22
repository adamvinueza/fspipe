from unittest.mock import mock_open, patch
from fspipe.pipe import Pipe


class TestPipe:

    @staticmethod
    def pass_through(rdr, wr, *params):
        while True:
            b = rdr.read()
            wr(b)
            if not b:
                break

    @staticmethod
    def fcopy_pass_through(b_in, first, second):
        result = b_in
        if first == 'dog':
            result += first.encode('utf8')
        if second == 'cat':
            result += second.encode('utf8')
        return result

    @patch('fsspec.implementations.local.LocalFileSystem')
    def test_init(self, local):
        tr = Pipe(src_fs=local, dest_fs=local)
        assert(tr is not None)
        assert(local == tr.src_fs)
        assert(local == tr.dest_fs)

    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    @patch("builtins.open", new_callable=mock_open)
    def test_copy(self, mock_fs_wopen, mock_fs_ropen, mock_write, mock_read):

        # Mock the writing file system
        mock_write.open = mock_fs_wopen
        mock_writer = mock_fs_wopen.return_value

        # Mock the reading file system
        mock_read.open = mock_fs_ropen
        mock_reader = mock_fs_ropen.return_value

        # mocked source and destination file
        src = 'src'
        dest = 'dest'

        tr = Pipe(src_fs=mock_read, dest_fs=mock_write)
        tr.copy(src, dest)

        # reading is binary
        mock_fs_ropen.assert_called_once_with(src, 'rb', -1)
        mock_reader.read.assert_called_once()

        # writing is binary
        mock_write.open.assert_called_once_with(dest, 'wb', -1)
        mock_writer.write.assert_called_once_with('data')

    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch('fsspec.implementations.local.LocalFileSystem')
    @patch("builtins.open", new_callable=mock_open, read_data=b"animal")
    @patch("builtins.open", new_callable=mock_open)
    def test_fcopy(self, mock_fs_wopen, mock_fs_ropen, mock_write, mock_read):

        # Mock the writing file system
        mock_write.open = mock_fs_wopen
        mock_writer = mock_fs_wopen.return_value

        # Mock the reading file system
        mock_read.open = mock_fs_ropen
        mock_reader = mock_fs_ropen.return_value

        # mocked source and destination file
        src = 'src'
        dest = 'dest'

        tr = Pipe(src_fs=mock_read, dest_fs=mock_write)
        tr.fcopy(src,
                 dest,
                 TestPipe.fcopy_pass_through,
                 first='dog',
                 second='cat')

        # reading is binary
        mock_fs_ropen.assert_called_once_with(src, 'rb', -1)
        assert(2 == mock_reader.read.call_count)

        # writing is binary
        mock_write.open.assert_called_once_with(dest, 'wb', -1)
        mock_writer.write.assert_called_once_with(b'animaldogcat')
