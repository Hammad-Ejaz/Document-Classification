import random
import networkx as nx
import gravis as gv
from graphs import create_topic_graphs
from sklearn.metrics import classification_report, confusion_matrix

def mcs(g1, g2):
    matching_graph = nx.Graph()

    for n1,n2 in g2.edges():
        if g1.has_edge(n1, n2):
            matching_graph.add_edge(n1, n2)

    components = list(nx.connected_components(matching_graph))

    if len(components) == 0:
        return nx.DiGraph()

    largest_component = max(components, key = len)
    return nx.induced_subgraph(g1, largest_component)

def distance(g1, g2):
    return 1 - len(mcs(g1, g2))/max(len(g1), len(g2))

def knn(train, test, k = 3):
    distances = []

    for graph in train:
        distances.append((distance(graph, test), graph))
    
    distances.sort(key = lambda x: x[0])
    return [d[1] for d in distances[:k]]

def classify(train, test):
    neighbours = knn(train, test)
    neighbours_categories = [neighbour.graph['category'] for neighbour in neighbours]

    occurences = {}

    for category in set(neighbours_categories):
        occurences[category] = neighbours_categories.count(category)
    
    return sorted(occurences.items(), key = lambda item: item[1], reverse = True)[0][0]

def train_test_split(data: list, train_ratio: float = 0.8):
    n = int(len(data) * (1 - train_ratio))

    train = data
    test = []

    for i in range(n):
        test.append(train.pop(random.randint(0, len(train) - 1)))
    
    return train, test

def run_model(data):
    train, test = train_test_split(data)

    predictions = []
    originals = list(map(lambda x: x.graph['category'], test))

    for i, sample in enumerate(test):
        predicted = classify(train, sample)
        predictions.append(predicted)

        # print(f"Predicted: {predicted} \t Original: {originals[i]}")
    
    return predictions, originals

def report_metrics(predictions, originals, model):
    print(f"{model} Metrics")
    print("Classfication report:")
    print(classification_report(originals, predictions))
    print("Confusion matrix:")
    print(confusion_matrix(originals, predictions))

if __name__ == '__main__':
    graphs = create_topic_graphs('Food')
    graphs.extend(create_topic_graphs('Sport'))
    graphs.extend(create_topic_graphs('Travel'))


    graph =  gv.vis(graphs, edge_label_data_source = "section")
    graph.display()
    predicted, originals = run_model(graphs)

    report_metrics(predicted, originals, "Graph-based kNN")