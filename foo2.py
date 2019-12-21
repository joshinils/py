from PIL import Image
import numpy as np
import os
from shutil import copyfile


class ImageFile:
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __lt__(self, other):
        return self.name < other.name


class FileReader:
    filenames = ''

    def __init__(self, path, diff_path, batch_size: int = 2) -> None:
        self.path = path
        self.diff_path = diff_path
        self.batch_size = batch_size

    def setup(self):
        self._ensure_diff_path()
        self._gen_filenames()

    def _ensure_diff_path(self) -> None:
        if not os.path.exists(self.diff_path):
            os.mkdir(self.diff_path)

    def _gen_filenames(self) -> None:
        self.filenames = [ImageFile(self.path, f) for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        self.filenames.sort()
        self.file_count = len(self.filenames)

    def process(self) -> None:
        file_generator = file_list(self.filenames, self.batch_size, self.file_count)
        for image_batch in file_generator:
            self._process_batch(image_batch)

    def _process_batch(self, images) -> None:
        # pre-process images
        print('pre-processing images')
        w, h = images[0][0].size
        s = 8
        w //= s
        h //= s
        for imList in images:
            # scale images down
            # todo thumbnail?
            imList[0].thumbnail((w, h))
        # break
        # imList[0] = imList[0].resize( (w, h) )

        # detect level of differences
        print('detecting differences')
        min_diff = 1000
        max_diff = 0
        num_diff = 0
        sum_iff = 0
        for index, imList in enumerate(images):
            if index == len(images) - 1:
                break
            print('\033[Kcomparing image', index, 'of', len(images), end=' ')
            buf1 = np.asfarray(imList[0])
            buf2 = np.asfarray(images[index + 1][0])

            buf3 = abs(buf1 - buf2)

            p = [0, 0, 0]
            for k in range(h):
                for j in range(w):
                    p += buf3[k][j]
            p /= w * h
            p = (p[0] + p[1] + p[2]) / 3
            print(' diff=', "% 7.3f" % p, end=' ')
            min_diff = min(min_diff, p)
            max_diff = max(max_diff, p)
            num_diff += 1
            sum_iff += p
            avg_diff = sum_iff / num_diff
            print("% 7.3f" % min_diff, "% 7.3f" % avg_diff, "% 7.3f" % max_diff, end='\r')

            do_save = bool((p >= 3))
            imList[2] |= do_save  # save this
            images[index + 1][2] = do_save  # save next
        print()  # to not overwrite the last output

        # count different images
        diffs = 0
        for imList in images:
            if imList[2]:
                diffs += 1

        # save images
        print('saving', diffs, 'images')
        for imList in images:
            if imList[2]:
                copyfile(self.path + imList[1], self.diff_path + imList[1])
            # imList[0].save(diffpath + imList[1])
        print('saving done')


def file_list(iterable, batch_size, max_items):
    num = 0
    while num < max_items:
        file_batch = []
        print(f'Opening {batch_size} images #{num + 1} - #{num + batch_size}')
        for i in range(num, min(max_items, num + batch_size)):
        yield file_batch
        num += batch_size


if __name__ == '__main__':
    client = FileReader('/mnt/kamera/20191210/', '/mnt/kamera/20191210/diffs')
    client.setup()
    client.process()
