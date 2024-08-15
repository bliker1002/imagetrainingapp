const { spawn } = require('child_process');
const path = require('path');

// Run the execution.py script
const pythonProcess = spawn('python', [path.join(__dirname, 'execution.py')]);

pythonProcess.stdout.on('data', (data) => {
  console.log(`Python script output: ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
  console.error(`Python script error: ${data}`);
});

pythonProcess.on('close', (code) => {
  console.log(`Python script exited with code ${code}`);
});

// The rest of your React setup code goes here
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Signup from './signup';
import Chat from './chat';
import 'bootstrap/dist/css/bootstrap.min.css';
import './custom.css';

function App() {
  return (
    <Router>
      <div className="app">
        <Switch>
          <Route exact path="/" component={Signup} />
          <Route path="/chat" component={Chat} />
        </Switch>
      </div>
    </Router>
  );
}

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);