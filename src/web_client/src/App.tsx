import * as React from 'react';
import './App.css';
import ReactRouter from './ReactRouter';

class App extends React.Component<any> {
    public render() {
        return (
            <div>
                <ul>
                    <li><a href="/">Main</a></li>
                    <li><a href="/profile">Profile</a></li>
                </ul>
                <ReactRouter />
            </div>
        );
    }
}

export default App;
