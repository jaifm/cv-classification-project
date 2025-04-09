# CV Classification and Skill Gap Analysis using Machine Learning

**Dissertation Project | Coventry University**\
**Author:** Jaidon Froggatt-Morton\
**SID:** 11191168\
**Academic Year:** 2024/2025

## Project Overview

The aim of this dissertation is to explore the effectiveness of machine learning algorithms—specifically **K-Nearest Neighbors (KNN)**, **Support Vector Machines (SVM)**, **Naive Bayes**, and **Decision Trees** and **BERT**—for classifying CVs (resumes). The best-performing algorithm will then be integrated into a **Flask-based web application**, providing students with personalised skill gap analysis and tailored recommendations to enhance employability.


## Aims and Objectives

- **Compare and evaluate** KNN, SVM, Naive Bayes, and Decision Tree algorithms.
- Evaluate models based on **accuracy, efficiency, and scalability**.
- Develop a prototype Flask-based web application.
- Provide students with actionable insights and recommendations through automated CV analysis and skill-gap identification.


## Project Structure

```text
cv-classification-project/
├── data/                   # Raw and processed datasets
├── notebooks/              # Jupyter notebooks for EDA and initial modelling
├── src/                    # Python scripts for preprocessing, training, and evaluation
│   ├── data_preprocessing.py
│   ├── train_models.py
│   ├── evaluate_models.py
│   └── model_utils.py
├── models/                 # Serialized trained models
├── app/                    # Flask web application
│   ├── static/
│   ├── templates/
│   │   └── index.html
│   ├── __init__.py
│   └── main.py
├── tests/                  # Testing code
└── docs/                   # Project documentation and reports

```

## Technical Stack

**Languages:**
- Python 3.9+
- HTML, CSS, JavaScript

**Libraries & Frameworks:**
- Flask
- Scikit-learn
- spaCy
- Pandas
- NumPy
- Matplotlib

**Database:**
- SQLite

**Development Tools:**
- Visual Studio Code (with Jupyter extension)
- Git (version control)
- Anaconda/Miniconda (environment management)

---

## Dataset

- **Source:** [Kaggle Resume Dataset](https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset)
- **Description:** Categorized resumes used for training and testing classification models.

---

## Getting Started

### Clone Repository

```bash
git clone https://github.com/jaifm/cv-classification-project.git
cd cv-classification-project
```
### Environment Setup
```bash
# Create and activate conda environment
conda create -n cv-env python=3.9
conda activate cv-env
```
### Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
### Running the Application
``` bash
cd app
python main.py
```
Visit http://127.0.0.1:5000 in your browser.

## Project Timeline

| Weeks | Tasks & Deliverables                                     |
|-------|----------------------------------------------------------|
| 1-2   | Data collection, preprocessing, and exploratory analysis |
| 3-4   | Initial model development and evaluation                 |
| 5-6   | Hyperparameter tuning and scalability testing            |
| 7-8   | Web application development (Flask prototype)            |
| 9-10  | Integration, documentation, and final dissertation       |


## Workflow

1. **Exploratory Data Analysis (EDA)**: Analyze data distribution, text cleaning, and initial insights.  
2. **Preprocessing Pipeline**: Use spaCy for text preprocessing, TF-IDF for feature extraction.  
3. **Model Development**: Train and evaluate ML models (KNN, SVM, Naive Bayes, Decision Tree).  
4. **Flask App Development**: Prototype and iterate on the Flask web application integrating your chosen model.  
5. **Testing and Documentation**: Ensure quality through tests and clearly document processes and results.

## References

All references are detailed in the full dissertation project document.

## Contact Information

- **Name:** Jaidon Froggatt-Morton
- **University:** Coventry University
- **Supervisor:** Ade Shonola

