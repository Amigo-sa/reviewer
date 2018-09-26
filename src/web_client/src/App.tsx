import * as React from "react";
import { Route, Switch } from "react-router";
import "./App.css";
import AddSurveyPage from "./pages/AddSurveyPage";
import Main from "./pages/Main";
import PersonalPage from "./pages/PersonalPage";
import SearchPeoplesPage from "./pages/SearchPeoplesPage";
import SearchStructuresPage from "./pages/SearchStructuresPage";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/loginPage";

class App extends React.Component<any> {
    public render() {
        return (
            <Switch>
                <Route exact={true} path="/" component={Main} />
                <Route path="/login" component={LoginPage} />
                <PrivateRoute path="/personal" component={PersonalPage} />
                <PrivateRoute path="/search-peoples" component={SearchPeoplesPage} />
                <PrivateRoute path="/search-structures" component={SearchStructuresPage} />
                <PrivateRoute path="/add-survey" component={AddSurveyPage} />
            </Switch>
        );
    }
}

export default App;
