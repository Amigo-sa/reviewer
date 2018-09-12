import * as React from 'react';
import { Route } from 'react-router';
import { BrowserRouter, Switch } from 'react-router-dom';
import Main from './components/Main';
import Profile from './components/Profile';

class ReactRouter extends React.Component<any> {
    public render() {
        return (
            <BrowserRouter>
                <Switch>
                    <Route exact={true} path="/" component={Main} />
                    <Route path="/profile" component={Profile} />
                </Switch>
            </BrowserRouter>
        );
    }
}

export default ReactRouter;
