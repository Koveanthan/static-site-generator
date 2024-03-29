import os
import shutil


def copy_static(src, dst):
    static_path = os.path.join(os.getcwd(), src)
    if os.path.exists(static_path):
        print(f"Directory(static) {static_path} present, proceeding with copy")
    else:
        print(f"Directory(static) {static_path} not present, aborting copy")
        return

    public_path = os.path.join(os.getcwd(), dst)
    if os.path.exists(public_path):
        print(f"Directory(pubilc) {public_path} exists, so cleaning and recreating it")
        shutil.rmtree(public_path)
        os.mkdir(public_path)
    else:
        print(f"Directory(pubilc) {public_path} doesn't exists, so creating it")
        os.mkdir(public_path)

    dirs = os.listdir(static_path)

    if dirs:
        for dir in dirs:
            if os.path.isdir(os.path.join(src, dir)):
                copy_static(os.path.join(src, dir), os.path.join(dst, dir))
            else:
                print(
                    f"copying file {os.path.join(src, dir)} to {os.path.join(dst,dir)}"
                )

                shutil.copy(os.path.join(src, dir), os.path.join(dst, dir))
