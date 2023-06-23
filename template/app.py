from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        # Your existing code here
        return render_template('index.html')
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    app.run()
