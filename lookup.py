# Import necessary modules
from flask import Flask, request, jsonify, render_template_string
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# HTML and JavaScript code as a single page served by Flask
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Truecaller Lookup</title>
  <style>
    /* Inline CSS */
    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      background-color: #121212;
      color: #FFD700;
      font-family: Arial, sans-serif;
    }
    h1 {
      margin-bottom: 20px;
    }
    input, button {
      padding: 10px;
      border-radius: 5px;
      border: 2px solid #FFD700;
      background-color: #1f1f1f;
      color: #FFD700;
      font-size: 16px;
      outline: none;
    }
    input {
      margin-bottom: 10px;
      width: 250px;
      text-align: center;
    }
    button {
      cursor: pointer;
    }
    .result {
      margin-top: 20px;
      text-align: center;
    }
    footer {
      position: absolute;
      bottom: 10px;
      color: #888;
    }
  </style>
</head>
<body>

  <h1>Truecaller Lookup</h1>
  <input type="text" id="phoneNumber" placeholder="Enter phone number">
  <button onclick="fetchData()">Lookup</button>
  
  <div class="result" id="result"></div>
  
  <footer>Developed by SA Team</footer>
  
  <script>
    // JavaScript function to fetch data from the Python server
    async function fetchData() {
      const phoneNumber = document.getElementById('phoneNumber').value;
      const resultDiv = document.getElementById('result');
      resultDiv.innerHTML = 'Loading...';

      try {
        const response = await fetch(`/api/truecaller?number=${phoneNumber}`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        resultDiv.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
      } catch (error) {
        resultDiv.innerHTML = `Error fetching data: ${error.message}`;
      }
    }
  </script>

</body>
</html>
"""

# Flask route to serve the HTML page
@app.route('/')
def index():
    return render_template_string(html_code)

# Flask route to handle API requests
@app.route('/api/truecaller', methods=['GET'])
def get_truecaller_data():
    number = request.args.get('number')
    if not number:
        return jsonify({"error": "Number is required"}), 400

    try:
        # Forward the request to the Truecaller API
        api_url = f"https://api.pikaapis.my.id/truecaller/?number={number}"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            return jsonify({"error": f"Error fetching data: {response.status_code}"}), response.status_code
        
        # Return the JSON response from the API
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
