from sklearn.svm import SVC  
from sklearn.feature_extraction.text import TfidfVectorizer
from classification import train_test_split, report_metrics;
import glob


def get_text_portion_from_file(filename):
    with open(filename, "r", encoding='utf-8') as fp:
        title = fp.readline()
        links = fp.readline()
        text = fp.readline()
    return text            

def vectorize_data(train, test):
    vectorizer = TfidfVectorizer()
    train_vector = vectorizer.fit_transform(train)
    test_vector = vectorizer.transform(test)
    return train_vector, test_vector

def annotator(topic: str):
    documents = []
    for filename in glob.glob(f"Scrapping/{topic}/file-*.txt"):  # Use '/' instead of '\\'
        text = get_text_portion_from_file(filename)
        documents.append({'vector': text, 'category': topic})  # Update each dictionary
    return documents
        
def run_model(data):
    train, test = train_test_split(data)

    train_vectors = [sample['vector'] for sample in train]
    train_categories = [sample['category'] for sample in train]
    test_vectors = [sample['vector'] for sample in test]
    
    train_vectors , test_vectors = vectorize_data(train_vectors,test_vectors)
 
    classifier = SVC()
    classifier.fit(train_vectors, train_categories)

    # Predict the categories for the test data
    predictions = classifier.predict(test_vectors)
    originals = [sample['category'] for sample in test]

    return predictions, originals

if __name__ == '__main__':
    documents = annotator('Food')
    documents.extend(annotator('Sport'))
    documents.extend(annotator('Travel'))

    predicted, originals = run_model(documents)

    report_metrics(predicted, originals, "Vector-based SVC")
