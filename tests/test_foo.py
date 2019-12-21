import os
import shutil
import tempfile
from unittest import TestCase, mock

from foo2 import FileReader, file_list


class FileReaderTestCase(TestCase):
    def setUp(self) -> None:
        self.path = tempfile.mkdtemp()
        self.diff_path = tempfile.mkdtemp()
        for i in range(5):
            setattr(self, f'file_{i}', tempfile.mkstemp(prefix=chr(i + 64), suffix='.png', dir=self.path)[1])

        self.file_reader = FileReader(self.path, self.diff_path)

    def tearDown(self) -> None:
        shutil.rmtree(self.path)
        shutil.rmtree(self.diff_path)

    @mock.patch('os.mkdir')
    @mock.patch('foo2.FileReader._gen_filenames')
    def test_setup_ensure_diff_path(self, gen_filenames_fake, mkdir_fake):
        FileReader('/tmp', '/tmp/diff').setup()

        mkdir_fake.assert_called_once()

    def test_setup_gen_filenames(self):
        self.file_reader.setup()

        self.assertEqual(self.file_reader.file_count, 5)

    def test_filenames_sort(self):
        self.file_reader.setup()

        self.assertEqual(self.file_reader.file_count, 5)
        for index, file in enumerate(self.file_reader.filenames):
            self.assertEqual(getattr(self, f'file_{index}'), os.path.join(file.path, file.name))

    @mock.patch('PIL.Image.open')
    def test_file_list_generator_batch_size(self, open_image_fake):
        self.file_reader.setup()
        batch_size = 2
        file_generator = file_list(self.file_reader.filenames, batch_size, self.file_reader.file_count)

        for batch in file_generator:
            self.assertLessEqual(len(batch), batch_size)

        self.assertEqual(open_image_fake.call_count, self.file_reader.file_count)

    @mock.patch('PIL.Image.open')
    def test_file_list_generator(self, open_image_fake):
        self.file_reader.setup()
        batch_size = 2
        file_generator = file_list(self.file_reader.filenames, batch_size, self.file_reader.file_count - 1)

        first_batch = file_generator.__next__()

        self.assertEqual(os.path.join(self.file_reader.path, first_batch[0][1]), getattr(self, 'file_0'))
