import * as React from "react";
import { Route, Switch } from "react-router";
import "./App.css";
import AddSurveyPage from "./pages/AddSurveyPage";
import Main from "./pages/Main";
import PersonalPage from "./pages/PersonalPage";
import SearchPeoplesPage from "./pages/SearchPeoplesPage";
import SearchStructuresPage from "./pages/SearchStructuresPage";

class App extends React.Component<any> {
    public render() {
        return (
            <Switch>
                <Route exact={true} path="/" component={Main} />
                <Route path="/personal" component={PersonalPage} />
                <Route path="/search-peoples" component={SearchPeoplesPage} />
                <Route path="/search-structures" component={SearchStructuresPage} />
                <Route path="/add-survey" component={AddSurveyPage} />
            </Switch>
        );
    }
}

export default App;
