import os
import torch
import matplotlib.pyplot as plt
from coco_dataset import COCODataset_ImageOnly
from img_caption_model import ImageCaptionModel
from torch.utils.data import DataLoader, Subset
from transformers import GPT2Tokenizer

'''
Forward pass the image caption model and save results
'''

# Path to save captioned images:
img_path = os.path.join('data', 'eval_data', 'val')
num_imgs = 8 # Number of images to caption

# Load validation data
dataset = COCODataset_ImageOnly(os.path.join('data', 'coco_data'), False)
dataloader = DataLoader(dataset, shuffle = True)

# Load caption generator
img_cap_model = ImageCaptionModel(os.path.join('models', 'unfrozen_gpt2', 'model_epoch2.pt'))
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# Sample images
i = 0
for img, id in iter(dataloader):
    i += 1
    if i > num_imgs:
        break

    # Pass through caption generator
    tokens, _ = img_cap_model(img)
    caption = tokenizer.decode(tokens).split('<|endoftext|>')[0]

    # Plot/show
    id = id.squeeze().item()
    img = img[0].permute(1, 2, 0).to(torch.uint8)
    plt.gca().axes.get_xaxis().set_ticks([])
    plt.gca().axes.get_yaxis().set_ticks([])
    plt.imshow(img)
    plt.xlabel(caption)
    plt.savefig(os.path.join(img_path, '{0}.jpg'.format(id)))

