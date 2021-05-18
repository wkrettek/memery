# AUTOGENERATED! DO NOT EDIT! File to edit: 01_loader.ipynb (unless otherwise specified).

__all__ = ['slugify', 'get_image_files', 'archive_loader', 'db_loader', 'treemap_loader']

# Cell
from pathlib import Path

# Cell
def slugify(filepath):
    return f'{filepath.stem}_{str(filepath.stat().st_mtime).split(".")[0]}'

def get_image_files(path):
    img_extensions = ['.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp']
    return [(f, slugify(f)) for f in path.rglob('*') if f.suffix in img_extensions]

# Cell
import torch
import torchvision

# Cell
def archive_loader(filepaths, root, device):
    dbpath = root/'memery.pt'
#     dbpath_backup = root/'memery.pt'
    db = db_loader(dbpath)

    current_slugs = [slug for path, slug in filepaths]
    archive_db = {k:db[k] for k in db if k in current_slugs}
    archive_slugs = [v['slug'] for v in archive_db.values()]
    new_files = [(str(path), slug) for path, slug in filepaths if slug not in archive_slugs]

    return(archive_db, new_files)

# Cell
def db_loader(dbpath):
    # check for savefile or backup and extract
    if dbpath.exists():
        db = torch.load(dbpath)
#     elif dbpath_backup.exists():
#         db = torch.load(dbpath_backup)
    else:
        db = {}
    return(db)

# Cell
from annoy import AnnoyIndex

# Cell
def treemap_loader(treepath):
    treemap = AnnoyIndex(512, 'angular')

    if treepath.exists():
        treemap.load(str(treepath))
    else:
        treemap = None
    return(treemap)