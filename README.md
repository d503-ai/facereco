# Facereco

**Facereco** is a web application designed for facial recognition and comparison tasks. It operates machine learning models and libraries to provide accurate and efficient face recognition capabilities. The application is built using the Django framework for Python and integrates libraries such as Dlib, OpenCV, and a custom-trained VGG16-based model (VGGImp). Facereco allows users to compare faces in images, analyze the impact of noise on recognition accuracy, and store results for future reference.

## Features

- **Facial Recognition**: Utilizes Dlib, OpenCV, and a custom VGG16-based model (VGGImp) for face recognition tasks.
- **Face Comparison**: Compares two images to determine if they contain the same person.
- **Noise Analysis**: Experimental research on the impact of noise (Gaussian, Laplacian, Poisson, and Impulse noise) on face recognition accuracy.
- **User Authentication**: Users can register, log in, and save their recognition results.
- **Noise Application**: Apply various types of noise to images to test recognition robustness.
- **Database Integration**: Uses SQLite3 to store uploaded images and recognition results.
- **Siamese Neural Network**: Implements a Siamese Neural Network architecture for face verification tasks.

## Usage
- **Register/Log In:** Create an account or log in to save your recognition results.
- **Upload Images:** Upload two images for face comparison.
- **Compare Faces:** The application will analyze the images and determine if they contain the same person.
- **Apply Noise:** Experiment with different types of noise to see their impact on recognition accuracy.
- **View Results:** Check the results page for detailed comparisons and performance metrics.

## Technologies Used
- **Backend:** Django (Python)
- **Machine Learning Libraries:** Dlib, OpenCV, VGGImp (custom VGG16-based model)
- **Database:** SQLite3
- **Frontend:** HTML, CSS, JavaScript (Django templates)
- **Development Environment:** PyCharm

## Experimental Results

The application was tested with various types of noise to evaluate the robustness of the face recognition models. Key findings include:
- **Dlib:** Performs best with Poisson and Impulse noise (31.60% and 61.30% accuracy, respectively).
- **SNN (Siamese Neural Network):** Excels with Laplacian and Gaussian noise (84.10% and 83.10% accuracy, respectively).
- **OpenCV:** Shows the worst performance across all noise types, with an average accuracy degradation of 42.42%.
- **VGGImp:** Most affected by Laplacian noise (29.38% accuracy degradation) but generally outperforms OpenCV.