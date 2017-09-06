from http.server import BaseHTTPRequestHandler, HTTPServer

# Handler Class
# indicates what code to execute based on type of http request sent on the server
class webserverHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("/hello"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ''
        output += '<html><body>Hello!</body></html>'
        self.wfile.write(output.encode())
        print(output)
        return

      if self.path.endswith("/hola"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        output = ''
        output += '<html><body>&#161Hola! <a href = "/hello" >Back to Hello</a></body></html>'
        self.wfile.write(output.encode())
        print(output)
        return

    except IOError:
      self.send_error(404, 'File Not Found %s' % self.path)


# main()
# instantiate server and specify on what port it will listen to
def main():
  try:
    port = 8080
    server = HTTPServer(('', port), webserverHandler)
    print("Web server running opn port %s" % port)
    server.serve_forever()

  except KeyboardInterrupt:
    print("^C entered, stopping web server...")
    server.socket.close()

if __name__ == '__main__':
  # run main() when interpreter executes script
  main()