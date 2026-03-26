import torch
from torchvision import transforms
from huggingface_hub import hf_hub_download
from architecture import ResNetLungCancer
from .config import DEVICE

# Set up preprocessing
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def load_model(model_path=None):
    """Load the trained model and weights. Can take a local path or download from HF."""
    if model_path is None:
        model_path = hf_hub_download(
            repo_id="daksh-bhardwaj/Epics-Lung-Report",
            filename="lung_cancer_detection_model.pth",
            repo_type="model"
        )
    
    model = ResNetLungCancer(num_classes=4)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE))
    model = model.to(DEVICE)
    model.eval()
    return model

def get_prediction(image, model):
    """Run preprocessing and inference on the input image."""
    input_tensor = preprocess(image).unsqueeze(0).to(DEVICE)
    
    with torch.no_grad():
        output = model(input_tensor)
    
    return output
