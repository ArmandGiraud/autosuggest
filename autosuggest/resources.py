#!/usr/bin/env python3
# coding: utf-8

"""
Functions to load proper data
"""

from pkg_resources import resource_filename
from pathlib import Path
import shutil


PKG_NAME_ = Path(__file__).parent.name


# ==========================
# Generic resource functions
# ==========================
def get_resource(path):
    """Return the Path instance of the desired resource file"""
    if not path.startswith('data/'):
        path = 'data/' + path
    return Path(resource_filename(PKG_NAME_, path))


def read_resource(path, as_bytes=False, encoding='utf-8'):
    """
    Read the resource file, eventually as bytes instead of text string (default to unicode)
    """
    p = get_resource(path)
    if as_bytes:
        return p.read_bytes()
    else:
        return p.read_text(encoding=encoding)


def copy_resource(path, dest, pattern='*'):
    """Copy a resource file to another destination"""
    src = get_resource(path)
    dest = Path(dest).expanduser().absolute()

    if src.is_file():
        if dest.is_dir():
            dest /= src.name
        elif not dest.exists():
            if not dest.suffix:
                dest /= src.name
        shutil.copy2(str(src), str(dest))

        return src

    else:
        if not dest.is_dir():
            assert not dest.exists(), '`dest` must be a directory, eventually not existing: cannot copy dir. resource'
            dest.mkdir(parents=True)

        files = src.glob(pattern)
        for name in files:
            shutil.copy2(str(name), str(dest / name.name), follow_symlinks=False)

        return files
