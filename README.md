# Deepfake Image Detection - Literature Review & Model Training

## 📌 Overview
Deepfake image and video detection is becoming increasingly crucial in today's digital age. With the rapid advancement of AI-driven content generation, distinguishing real from synthetic media is essential to combat misinformation, fraud, and digital manipulation. From social media to political campaigns, deepfakes have the potential to mislead the public, making robust detection methods a necessity for maintaining digital integrity. This repository documents my **literature review** and **hands-on training** of multiple deep learning architectures to evaluate their effectiveness in detecting deepfake images and videos.

## 📊 Dataset Overview
The dataset used in this study consists of images categorized into three sets: training, testing, and validation. Each set is further divided into two classes: real and fake. The breakdown is as follows:

* Training Set: 6400 images (50% real, 50% fake)
* Testing Set: 800 images (50% real, 50% fake)
* Validation Set: 800 images (50% real, 50% fake)
### 📌 Train : Test : Validation Ratio → 8:1:1

All images in the dataset are facial images, ensuring that the models learn to detect manipulations in facial structures effectively.

### 🏆 Significance of the Ratio
The 8:1:1 split is chosen to provide an optimal balance between training efficiency and model evaluation:
* ✅ 80% Training Data → Allows deep learning models to generalize patterns effectively.
* ✅ 10% Validation Data → Helps in fine-tuning hyperparameters and preventing overfitting.
* ✅ 10% Testing Data → Evaluates model performance on unseen data, ensuring real-world applicability.

This structured division ensures that the model learns well, generalizes efficiently, and maintains robustness in detecting deepfake images. 🚀

## 🚀 Deep Learning Models Explored
I have implemented and trained the following models for deepfake image detection:

### 1️⃣ **Xception Net**
* ✅ Advantage: **Separable convolutions** allow for better feature extraction with fewer parameters, making it highly efficient in detecting subtle facial manipulations.
* ✅ Performance: Achieved **88% precision** and **85% recall** after training.

### 2️⃣ **VGG-19**
* ✅ Advantage: **Deep architecture** with small convolutional filters (3x3), making it effective at capturing intricate details in images.
* ✅ Performance: Achieved **86% precision, recall, and F1-score** in detection tasks.

### 3️⃣ **ResNet-50**
* ✅ Advantage: **Residual connections** solve the vanishing gradient problem, ensuring deeper networks learn effectively without degradation.
* ✅ Performance: Achieved **83% precision, recall, and F1-score**, balancing efficiency and accuracy.

### 4️⃣ **CViT (Convolutional Vision Transformer)**
* ✅ Advantage: **Hybrid approach** combining CNNs and Transformers for improved spatial relationships and contextual understanding.
* ✅ Performance: Demonstrated promising accuracy but required fine-tuning for optimal results.

### 5️⃣ **CNN-LSTM**
* ✅ Advantage: **Temporal sequence learning** capability allows detection of inconsistencies across frames in video-based deepfake detection.
* ✅ Performance: Achieved **81% precision and 78% F1-score**, effective for sequential image-based deepfake detection.

## 📊 Model Performance Summary
The following table presents the performance metrics obtained after training:

| Model       | Precision | Recall | F1-Score | Accuracy |
|------------|-----------|---------|----------|----------|
| **VGG-19**        | 0.86  | 0.86  | 0.86  | 0.86  |
| **CViT Model**    | 0.80  | 0.79  | 0.79  | 0.79  |
| **ResNet-50**     | 0.83  | 0.83  | 0.83  | 0.83  |
| **Xception Net**  | 0.88  | 0.85  | 0.85  | 0.85  |
| **CNN-LSTM**      | 0.81  | 0.79  | 0.78  | 0.79  |

## 🔬 Key Takeaways
- **Xception Net** outperformed other models in precision, making it a strong candidate for deepfake detection.
- **VGG-19 and ResNet-50** maintained high accuracy, proving their robustness.
- **CNN-LSTM**, though slightly lower in precision, is beneficial for video-based deepfake detection.
- **CViT** shows potential but requires further fine-tuning for improved performance.

## 📂 Repository Structure
```
├── data/               # Dataset used for training & evaluation
├── models/             # Trained model weights & architectures
├── notebooks/          # Jupyter notebooks for training & analysis
├── scripts/            # Python scripts for preprocessing & training
├── results/            # Performance metrics and visualizations
└── README.md           # This document
```

## 📢 Future Work
-  Expanding research into **deepfake video detection**, as image-based detection alone is insufficient to combat evolving generative techniques.
-  As a starting point, I have explored **CNN-LSTM hybrid models** to analyze sequential frame inconsistencies in videos.
-  Experimenting with **3D CNNs and Transformer-based models** for improved spatiotemporal feature extraction.

## 💡 Contributing
If you're interested in improving deepfake detection methodologies or have insights into advanced architectures, feel free to contribute!


