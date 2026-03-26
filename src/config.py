import torch

# 1. Setup Device
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

CLASS_NAMES = ['Adenocarcinoma', 'Large Cell Carcinoma', 'Normal', 'Squamous Cell Carcinoma']

# Explanations for each class
CANCER_EXPLANATIONS = {
    'Adenocarcinoma': "### 🩺 Understanding Adenocarcinoma\nAdenocarcinoma is the most common type of non-small cell lung cancer. It often begins in the outer regions of the lungs in cells that secrete substances such as mucus. \n\n**What this means:** While hearing this can be concerning, adenocarcinoma tends to grow more slowly than other types of lung cancer and is often found before it has spread outside the lung. Your healthcare team will discuss the best next steps, which may include further imaging or a biopsy to confirm.",
    'Large Cell Carcinoma': "### 🩺 Understanding Large Cell Carcinoma\nLarge Cell Carcinoma is a type of non-small cell lung cancer that can occur in any part of the lung. It is named for how the cancer cells look large and distinctly abnormal under a microscope.\n\n**What this means:** This type of cancer tends to grow and spread more quickly than some other forms, which means prompt follow-up is very important. Please consult your pulmonologist or oncologist immediately for a definitive diagnosis and to create a tailored care plan.",
    'Normal': "### ✅ Normal Scan Results\n**Great news:** The analysis of your scan indicates a healthy lung, with no signs of the specific carcinomas evaluated by this tool.\n\n**What this means:** Your lungs appear clear based on this image. However, remember that no AI analysis replaces a professional medical diagnosis. Continue your routine check-ups with your doctor, and reach out to them if you are experiencing any respiratory symptoms.",
    'Squamous Cell Carcinoma': "### 🩺 Understanding Squamous Cell Carcinoma\nSquamous Cell Carcinoma typically starts in the flat cells that line the inside of the airways (the bronchi) in the central part of the lungs.\n\n**What this means:** This condition is often linked to a history of smoking. Early detection is key, and the next typical step involves speaking closely with your doctor to confirm the findings—often through additional imaging or a biopsy—and discussing your treatment options."
}
