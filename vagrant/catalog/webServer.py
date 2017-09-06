from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations
from db_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session & connect to db
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Handler Class
# indicates what code to execute based on type of http request sent on the server
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add New Restaurant Here</a>"
                output += "</br>"
                output += "</br>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='#'>Edit</a>"
                    output += "</br>"
                    output += "<a href='#'>Delete</a>"
                    output += "</br>"
                    output += "</br>"

                output += "</body></html>"
                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Add new restaurant"
                output += "</br>"
                output += "</br>"

                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'> <h2>Add New</h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"

                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body> Hello!"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> <h2>What would you like me to say?</h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"

                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>&#161Hola! <a href = '/hello'>Back to Hello</a>"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> <h2>What would you like me to say?</h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"

                output += "</body></html>"

                self.wfile.write(output.encode())
                print(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers['Content-type'])

            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')[0].decode('utf-8')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent

            output += "<form method='POST' enctype='multipart/form-data' action='/hello'> <h2>What would you like me to say?</h2> <input name='message' type='text'> <input type='submit' value='Submit'> </form>"

            output += "</body></html>"

            self.wfile.write(output.encode('utf-8'))
            print(output)

        except:
            pass


# main()
# instantiate server and specify on what port it will listen to
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    # run main() when interpreter executes script
    main()


'''
OBJECTIVES:

1. list out all restaurants
    [x] localhost:8080/restaurants
2. add, edit, & delete links
    [x] after the name of each db there are links to edit & delete
3. create new restaurants
    [] there is a page with a form to create a new restaurant
    [] localhost:8080/restaurants/new
4. rename a restaurant
    [] users can rename a restaurant by visiting
    [] localhost:8080/restaurants/id/edit
5. delete a restaurant
    [] clicking delete takes user to confirmation page that sends 
    POST cmd to db to delete selected restaurant

'''

# need to import modules used for CRUD commands
# redesign do_GET & do_POST for needed CRUD ops


