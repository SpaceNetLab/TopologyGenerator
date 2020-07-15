# -*- coding:utf-8 -*-
import os
import errno


def create_file_if_not_exit(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

def main():
    print("Generating random object in objects folder.")
    filename_list = [];
    filename_list.append(("objects/random_1K.data", 1024))
    filename_list.append(("objects/random_10K.data", 1024*10))
    filename_list.append(("objects/random_100K.data", 1024*100))
    filename_list.append(("objects/random_1M.data", 1024*1024))

    for filename in filename_list:
        name = filename[0];
        size = filename[1];
        create_file_if_not_exit(name)
        f = open(name, "wb+")
        data = os.urandom(size)
        f.write(data)
        f.flush()
        print("Writing %s bytes random data to object." % (str(size)))
        f.close()

    print("Done.")


if __name__== "__main__":
    main();