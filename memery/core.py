# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['indexFlow', 'queryFlow']

# Cell
import torch
from pathlib import Path
from .loader import get_image_files, archive_loader, db_loader, treemap_loader
from .crafter import crafter
from .encoder import image_encoder, text_encoder
from .indexer import join_all, build_treemap, save_archives
from .ranker import ranker

# Cell
def indexFlow(path):
    root = Path(path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    filepaths = get_image_files(root)
    archive_db = {}

    archive_db, new_files = archive_loader(filepaths, root, device)
    print(f"Loaded {len(archive_db)} encodings")
    print(f"Encoding {len(new_files)} new images")
    crafted_files = crafter(new_files, device)
    new_embeddings = image_encoder(crafted_files, device)

    db = join_all(archive_db, new_files, new_embeddings)
    print("Building treemap")
    t = build_treemap(db)

    print(f"Saving {len(db)}images")
    save_paths = save_archives(root, t, db)
    print("Done")
    return(save_paths)

# Cell
def queryFlow(path, query):
    root = Path(path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dbpath = root/'memery.pt'
    db = db_loader(dbpath)
    treepath = root/'memery.ann'
    treemap = treemap_loader(treepath)

    if treemap == None or db == {}:
        dbpath, treepath = indexFlow(root)
        treemap = treemap_loader(Path(treepath))
        db = file

    print(f"Searching {len(db)} images")
    query_vec = text_encoder(query, device)
    indexes = ranker(query_vec, treemap)
    ranked_files = [[v['fpath'] for k,v in db.items() if v['index'] == ind] for ind in indexes]
    return(ranked_files)

