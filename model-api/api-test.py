from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/print_list', methods=['POST'])
def print_list():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400

        if 'list' not in data:
            return jsonify({'error': 'The "list" key is missing in the JSON data'}), 400

        # Extract the list from the JSON data
        input_list = data['list']

        # Print the list
        print(input_list)

        return jsonify({'message': 'List printed successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)