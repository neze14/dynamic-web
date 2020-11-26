# import Flask
from flask import Flask, render_template

# initialise app variable
app = Flask(__name__)


# decorate a python function with app.route. It  associates a web url with a defined function.
@app.route("/")
def home():
      return "This is the home, attached to root url /"


@app.route("/hello")
def hello():
      return "Hello World from Python Flask Web Framework!"


# function below will be called when the user adds a string after /hello/
# to the website address e.g /hello/pius/.
# That added string will be captured using a variable
# called name as shown below. Note that the variable does not
# have to be called name. It is simply convenient to use it here.
@app.route("/hello/<string:name>/")
def hello_with_person_name(name):
      # The two lines below will work. But the second is more convenient as it
      # implicitly identifies whether the variable is a string or number, etc

      # return "Hello %s, greetings from Flask Framework!" % name
      return "Hello {}, greetings from Python Flask Web Framework!".format(name)


# In the function below, the name passed will be used inside
# a template file called hello.html. We shall see what
# template engine options exist. For now we'll use Jinja2.
# The template file should be inside a folder called
# templates. Notice the call to the function render_template which we have imported.
@app.route("/hello2/<string:name>/")
def hello_with_template(name):
    return render_template('hello.html', person_name=name)


# Let's use a more complex template with inheritance.
# Two templates are involved here - hello-with-layout.html and
# layout.html. hello-with-layout.html inherits layout.html.
# We'll therefore only refer to the former in this python
# function.
@app.route("/hello3/<string:name>/")
def hello_with_layout(name):
    return render_template('hello-extend-layout.html', person_name=name)


# run the app notice here that we can specify host. 0.0.0.0 means that the app will be accessible from all the IP
# addresses on the system including 127.0.0.1 which is localhost. The default port for Flask is 5000. You can use
# something else.

if __name__ == "__main__":
    app.run()
    # or use more detailed app.run(host="0.0.0.0", port=int("5000"), debug=True