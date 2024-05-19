import argparse
from flask import Flask, request 
from src.index_creater import index_initializer
from src.utils import DocumentProcessor



app = Flask(__name__)

@app.route('/documents', methods=['GET'])
def document_search_route():
    query = request.args.get('query')
    normalized_query = preprocessor.process(query)
    result = inverted_index.search(normalized_query)
    
    return [x[1] for x in result]


@app.route('/indexes', methods=['GET'])
def indices_search_route():
    query = request.args.get('query')
    normalized_query = preprocessor.process(query)
    result = inverted_index.search(normalized_query)
    return [x[0] for x in result]
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-p','--database_path', 
                        help='Path to existing database', 
                        required=False)
    
    parser.add_argument('-m', '--methods', 
                        help='Methods of preprocessing documents',
                        required=False,
                        default=['lowcase', 'normalize_spaces', 'special_chars'])

    args = parser.parse_args()

    preprocessor = DocumentProcessor(methods=args.methods)
    inverted_index = index_initializer(args.database_path, preprocessor=preprocessor)

    app.run()


