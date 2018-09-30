import * as React from "react";
import { Route, Switch } from "react-router";
import "./App.css";
import AddSurveyPage from "./pages/AddSurveyPage";
import Main from "./pages/Main";
import PersonalPage from "./pages/PersonalPage";
import SearchPeoplesPage from "./pages/SearchPeoplesPage";
import SearchStructuresPage from "./pages/SearchStructuresPage";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import AuthorizationUIHelper from "./AuthorizationUIHelper";
import authStore from "./stores/AuthStore";

const authUIHelper = new AuthorizationUIHelper(authStore);

class App extends React.Component<any> {
    public render() {
        return (
            <Switch>
                <Route exact={true} path="/" component={Main} />
                <Route path="/login" component={LoginPage} />
                <PrivateRoute path="/personal" component={PersonalPage} authHelper={authUIHelper} />
                <PrivateRoute path="/search-peoples" component={SearchPeoplesPage} authHelper={authUIHelper} />
                <PrivateRoute path="/search-structures" component={SearchStructuresPage} authHelper={authUIHelper} />
                <PrivateRoute path="/add-survey" component={AddSurveyPage} authHelper={authUIHelper} />
            </Switch>
        );
    }
}

export default App;
