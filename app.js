
var express = require('express');
var http = require('http');
var fs = require('fs'); // Add this line

var app = express();
var server = http.createServer(app);

var io = require('socket.io')(server);
var path = require('path');

// Delete the context.json file if it exists
fs.unlink(path.join(__dirname, 'context.json'), (err) => {
  if (err) {
    if (err.code === 'ENOENT') {
      // File didn't exist, but that's fine
    } else {
      console.error(`Error deleting context.json: ${err}`);
    }
  } else {
    console.log('Successfully deleted context.json');
  }
});
app.use(express.static(path.join(__dirname,'./public')));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

var name;
var child_process = require('child_process');

// start the python script
var process = child_process.spawn('python', ['./simple_chat.py', "Hello"]);


io.on('connection', (socket) => {
  console.log('new user connected');

  // when the server starts, the first user to connect will be the "host"
  if (name == null) {
    var process = child_process.spawn('python', ['./simple_chat.py', "Hello"]);
  }
  
  socket.on('joining msg', (username) => {
  	name = username;
  	io.emit('chat message', `---${name} joined the chat---`);
    console.log('user joined:', name);
  });
  
  socket.on('disconnect', () => {
    console.log('user disconnected');
    io.emit('chat message', `---${name} left the chat---`);
    
  });
  /// write chats to python script through command line
  socket.on('chat message', (msg) => {
    //sending message to all except the sender
    socket.broadcast.emit('chat message', msg); 
    
    // print the text to our node.js console
    // need this to send messagaes to the chat instance
    process.stdin.write(msg + '\n');
  });
  process.stdout.on('data', function(data) {
    var message = data.toString();
    if (message.startsWith("LOG: ")) {
      console.log(message.slice(5));
    } else {
      io.emit('chat message', message);
      console.log(message);
    }
  });
});

// print the python errors to the console
process.stderr.on('data', function(data) {
  console.error(`Python error: ${data}`);
});

server.listen(3000, () => {
  console.log('Server listening on :3000');
});