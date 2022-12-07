from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

class WebServer:
    def __init__(self, configuration) -> None: 
        self.configuration = configuration # HOST, PORT
        self._logWhatString = "WebServer"
        self._directory = "build"
        self.flaskApp = Flask(
            name, 
            static_url_path='',
            static_folder=self._directory, 
            template_folder=self._directory)

        self.flaskApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self.cors = CORS(self.flaskApp)
        self.flaskApp.config['CORS_HEADERS'] = 'Content-Type'
        self.socketio = SocketIO(self.flaskApp, cors_allowed_origins = "*")


        self.defineRoutes()
        self.defineSocketIOEvents()

        self.sendTimeoutSocket = 0
        self.consoleMessages = []
        self.sendConsoleMessagesTimeout = 0

        self.mainThread = threading.Thread(target=self.startServer)
        try:
            self.mainThread.start()
        except KeyboardInterrupt:
            Console.info("Web Server closed", what="Web Server")
            try:
                exit(0)
            except SystemExit:
                os._exit(0)
        Console.success("Web Server Started", "[http://127.0.0.1:"+str(self.configuration.port)+"]", what=self._logWhatString)
    
    def stopServer(self):
        self.socketio.stop()
        sys.exit(0)

    def startServer(self):
        try:
            self.socketio.run(self.flaskApp, host= '0.0.0.0', port=self.configuration.port, debug=False)
            #serve(self.flaskApp, host= '0.0.0.0', port=self.configuration.port)
            # TODO MANAGE THE STOP OF SERVER
        except KeyboardInterrupt:
            Console.info("Web Server closed", what="Web Server")
            try:
                exit(0)
            except SystemExit:
                sys.exit(0)
        

    def defineSocketIOEvents(self):
        @self.socketio.on('connect')
        def onConnect():
            Console.info("Web Client Connected (socketIO)", what=self._logWhatString)

        @self.socketio.on('disconnect')
        def onDisconnect():
            Console.info("Web Client Disconnected (socketIO)", what=self._logWhatString)
        @self.socketio.on('ping')
        def onPing():
            self.socketio.emit("pong")
            Console.info("Web Client Disconnected (socketIO)", what=self._logWhatString)

    def defineRoutes(self):
        
        @self.flaskApp.route("/<path:path>")
        def staticDir(path):
            return send_from_directory(directory=self._directory, path=path)

        @self.flaskApp.route('/')
        def home():
            return render_template('index.html')


        @self.flaskApp.get("/version")
        @cross_origin()
        def getVersion():
            return Globals.applicationInstance.VERSION

        @self.flaskApp.route('/')
        def index():
            target_list = target.query.all() # SELECT * FROM target;
            print(target_list)

            return render_template('index.html', target_list=target_list)

        # @self.flaskApp.get("/version")
        # @self.flaskApp.post("/add")
        @app.route('/add', methods=['POST'])
        def add():
            # Add new target to the database
            sleep(3) # Delay useful to display form animation
            target_name = request.form.get('target_name')

            # X, Y, Theta will be returned from the setup_point() in robot.py
            # target_x = request.form.get('x')
            # target_y = request.form.get('y')
            # target_theta = request.form.get('theta')

            new_target = target(text=target_name, x=0, y=0, theta=0)
            db.session.add(new_target)
            db.session.commit()
            return redirect(url_for('index'))

        @app.route('/delete/<int:id>')
        def delete(id):
            # Add new target to the database
            item = target.query.filter_by(id=id).first()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('index'))

        


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    theta = db.Column(db.Integer)



if (__name__ == "__main__"):
    app.app_context().push()
    db.create_all()

    pepper = Pepper(config.IP_ADDRESS, config.PORT)

    app.run(debug=True)
