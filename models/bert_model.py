import pandas as pd
import re
from sklearn.model_selection import train_test_split
from transformers import TFBertForSequenceClassification, BertTokenizer
import tensorflow as tf
import os

# Load the dataset
data_path = r"C:\Users\ItsLo\Desktop\Dissertation\Project\cv-classification-project\data\resume_data.csv"
df = pd.read_csv(data_path)

# Data cleaning and preprocessing
def preprocess_data(df):
    # Convert text to lowercase
    df['Resume_str'] = df['Resume_str'].str.lower()
    
    # Replace special characters, punctuation, and numbers with whitespace
    df['Resume_str'] = df['Resume_str'].apply(lambda x: re.sub(r'[^a-zA-Z\s]', ' ', x))
    
    # Calculate the length of each CV in terms of word count
    df['resume_length'] = df['Resume_str'].apply(lambda x: len(str(x).split()))
    
    # Define thresholds for filtering resumes
    min_threshold = 1  # Remove resumes with 0 words
    max_threshold = 2000  # Example threshold for very long resumes
    
    # Filter the dataset based on thresholds
    df = df[(df['resume_length'] >= min_threshold) & (df['resume_length'] <= max_threshold)]
    
    return df

df = preprocess_data(df)

# Tokenize the data
def tokenize_data(texts, labels, max_len, tokenizer):
    encodings = tokenizer(texts.tolist(), truncation=True, padding='max_length', max_length=max_len, return_tensors='tf')
    dataset = tf.data.Dataset.from_tensor_slices((dict(encodings), labels))
    return dataset

# Set parameters
max_len = 128
num_labels = df['Category'].nunique()
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Split the data
X = df['Resume_str']
y = pd.factorize(df['Category'])[0]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Prepare datasets
train_dataset = tokenize_data(X_train, y_train, max_len, tokenizer).shuffle(1000).batch(16)
test_dataset = tokenize_data(X_test, y_test, max_len, tokenizer).batch(16)

# Build and compile the BERT model
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)
optimizer = tf.keras.optimizers.Adam(learning_rate=5e-5)
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])

# Train the model
model.fit(train_dataset, epochs=3, verbose=1)

# Evaluate the model
results = model.evaluate(test_dataset)
print(f"Test Loss: {results[0]}, Test Accuracy: {results[1]}")

# Save the model
save_path = "../models/saved_bert_model"
os.makedirs(save_path, exist_ok=True)
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print(f"Model and tokenizer saved to {save_path}")