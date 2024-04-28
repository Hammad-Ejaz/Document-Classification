import re, glob
import gravis as gv
import networkx as nx
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def remove_alphanumeric_symbols(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-zA-z\s]", "", s))

def remove_stopwords(tokens: list[str]):
    stop_words = stopwords.words("english")
    return list(filter(lambda x: x not in stop_words, tokens))

def get_tokens(s: str, remove_symbols: bool = True) -> list[str]:
    wnl = WordNetLemmatizer()

    if remove_symbols:
        s = remove_alphanumeric_symbols(s)

    return list(map(wnl.lemmatize, word_tokenize(s.lower())))


def get_nodes(title, links, text):
    nodes = get_tokens(title)

    for link in links:
        nodes.extend(get_tokens(link))    

    text_tokens = set(get_tokens(text))

    nodes = set(nodes).union(text_tokens)
    return remove_stopwords(nodes)

def process_section_tokens(graph: nx.MultiDiGraph, tokens: list[str], section: str):
    for i in range(1, len(tokens)):
        u = remove_alphanumeric_symbols(tokens[i - 1])
        v = remove_alphanumeric_symbols(tokens[i])

        if len(u) == 0 or len(v) == 0:
            continue
        
        graph.add_edge(u, v, section = section)

def create_graph(title, links, text):
    graph = nx.DiGraph()

    graph.add_nodes_from(get_nodes(title, links, text))

    # Title Section
    process_section_tokens(graph, remove_stopwords(get_tokens(title, False)), "title")

    # Links Section
    for link in links:
        process_section_tokens(graph, remove_stopwords(get_tokens(link, False)), "link")
    
    # Text Section
    process_section_tokens(graph, remove_stopwords(get_tokens(text, False)), "text")
    
    # return gv.vis(graph, edge_label_data_source = "section")
    return graph

def create_graph_from_file(filename):
    with open(filename, "r", encoding='utf-8') as fp:
        title = fp.readline()
        links = fp.readline()[:-1].split(",")
        links = list(filter(lambda x: not x.startswith("http"), links))
        text = fp.readline()

        return create_graph(title, links, text)

def create_topic_graphs(topic: str):
    graphs = [create_graph_from_file(file) for file in glob.glob(f"Scrapping\\{topic}\\file-*.txt")]
    
    for graph in graphs:
        graph.graph.update({'category': topic})

    return graphs

def export_graph(graph: nx.DiGraph):
    lines = []

    for node in graph.nodes:
        lines.append(f"v {node} 1")

    for edge in graph.edges.data('section'):
        lines.append(f"e {edge[0]} {edge[1]} {edge[2]}")
    
    return lines

def export_graphs(graphs: list, filename: str):
    lines = []

    for i, graph in enumerate(graphs):
        lines.append(f"t # {i}")
        lines.extend(export_graph(graph))
    
    with open(filename, "w+") as fp:
        fp.writelines([line + '\n' for line in lines])

def create_topic_graphs_data(topic: str):
    export_graphs(create_topic_graphs(topic), f"graphdata_{topic}.dat")

# create_topic_graphs_data("Food")