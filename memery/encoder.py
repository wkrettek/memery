# AUTOGENERATED! DO NOT EDIT! File to edit: 03_encoder.ipynb (unless otherwise specified).

__all__ = ['device', 'model', 'image_encoder', 'text_encoder', 'image_query_encoder']

# Cell
import torch
import clip
from tqdm import tqdm
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, _ = clip.load("ViT-B/32", device, jit=False)
model = model.float()

# Cell
def image_encoder(img_loader, device):
    image_embeddings = torch.tensor(()).to(device)
    with torch.no_grad():
        for images, labels in tqdm(img_loader):
            batch_features = model.encode_image(images)
            image_embeddings = torch.cat((image_embeddings, batch_features)).to(device)

    image_embeddings = image_embeddings / image_embeddings.norm(dim=-1, keepdim=True)
    return(image_embeddings)

# Cell
def text_encoder(text, device):
    with torch.no_grad():
        text = clip.tokenize(text).to(device)
        text_features = model.encode_text(text)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return(text_features)

# Cell
def image_query_encoder(image, device):
    with torch.no_grad():
        image_embed = model.encode_image(image.unsqueeze(0))
    image_embed = image_embed / image_embed.norm(dim=-1, keepdim=True)
    return(image_embed)