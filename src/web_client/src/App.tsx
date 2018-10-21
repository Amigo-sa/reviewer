import * as React from "react";
import { Route, Switch } from "react-router";
import "./App.css";
import AddSurveyPage from "./pages/AddSurveyPage";
import Main from "./pages/MainPage/Main";
import PersonalPage from "./pages/PersonalPage";
import SearchPeoplePage from "./pages/SearchPeoplePage";
import SearchStructuresPage from "./pages/SearchStructuresPage";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import AuthorizationUIHelper from "./AuthorizationUIHelper";
import authStore from "./stores/AuthStore";
import Grid from "@material-ui/core/Grid";

const authUIHelper = new AuthorizationUIHelper(authStore);

class App extends React.Component<any> {
    public render() {
        return (
            <div
                style={{
                    maxWidth: 1440,
                    minHeight: "100%",
                    margin: "0px auto",
                }}
            >
                <Grid container={true}>
                    <Switch>
                        <Route exact={true} path="/" component={Main} />
                        <Route path="/login" component={LoginPage} />
                        <PrivateRoute
                            path="/personal"
                            component={PersonalPage}
                            authHelper={authUIHelper}
                        />
                        <Route
                            path="/search-peoples"
                            component={SearchPeoplePage}
                            authHelper={authUIHelper}
                        />
                        <PrivateRoute
                            path="/search-structures"
                            component={SearchStructuresPage}
                            authHelper={authUIHelper}
                        />
                        <PrivateRoute
                            path="/add-survey"
                            component={AddSurveyPage}
                            authHelper={authUIHelper}
                        />
                    </Switch>
                </Grid>
            </div>
        );
    }
}

export default App;
