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
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import HeaderMenu from "./components/Menu";

const authUIHelper = new AuthorizationUIHelper(authStore);

class App extends React.Component<any> {
    public render() {
        return (
            <Grid
                container={true}
                spacing={24}
            >
                <Grid
                    item={true}
                    xs={12}
                >
                    <HeaderMenu />
                </Grid>
                <Grid
                    item={true}
                    xs={12}
                >
                    <Paper>
                        <Switch>
                            <Route exact={true} path="/" component={Main} />
                            <Route path="/login" component={LoginPage} />
                            <PrivateRoute
                                path="/personal"
                                component={PersonalPage}
                                authHelper={authUIHelper}
                            />
                            <PrivateRoute
                                path="/search-peoples"
                                component={SearchPeoplesPage}
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
                    </Paper>
                </Grid>
            </Grid>

        );
    }
}

export default App;
