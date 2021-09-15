from api import API

app = API()

@app.route("/home")
def home(request, response):
    response.text ="Hello from the HOME page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from the about page"

# @app.route("/about")
# def about(request, response):
#     response.text = "Fuck"

@app.route("/")
def index(request, response):
    response.text = "Welcome, my friend"

@app.route("/hello/{name}")
def hellothere(request, response, name):
    response.text = f"Hello there ~ {name}"


@app.route('/book')
class Book():

    def get(self, request, response):
        response.text = f"I am a get from book"

    def post(self, request, response):
        response.text = f"I am a post from book"