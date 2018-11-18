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
import authStore from "./model/AuthStore";
import Grid from "@material-ui/core/Grid";
import commonStore from "./model/CommonStore";
import Reviews from "./pages/ReviewPage";
import CreateReviewPage from "./pages/ReviewPage/CreateReviewPage";
import { LinearProgress } from "@material-ui/core";

interface IState {
    loaded: boolean;
}

class App extends React.Component<any, IState> {

    public state = {
        loaded: false,
    };

    public componentDidMount() {

        const loadCommonData = commonStore.loadData();
        const tryAuthorizate = authStore.tryAuthenticate();

        Promise.all([loadCommonData, tryAuthorizate]).then(() => {
            this.setState({ loaded: true });
        },
            () => {
                console.error("Inital loading error");
            });
    }

    public render() {
        if (this.state.loaded) {
            // If all initial data is loaded, then show application UI
            return (
                <div
                    style={{
                        maxWidth: 1440,
                        minHeight: "100%",
                        margin: "0px auto",
                    }}
                >
                    <Grid container>
                        <Switch>
                            <Route exact path="/" component={Main} />
                            <Route path="/login" component={LoginPage} />
                            {/* Change to private router */}
                            <PrivateRoute
                                exact
                                path="/personal"
                                component={PersonalPage}
                                authInfo={authStore.authInfo}
                            />
                            {/* TODO необходимо переносить роуты внутрь управляющих страниц! */}
                            {/* TODO: why do we use review url for current person? */}
                            <PrivateRoute
                                exact
                                path="/personal/:id/review"
                                component={CreateReviewPage}
                                authInfo={authStore.authInfo}
                            />
                            <PrivateRoute
                                path="/personal/:id/review/:specid"
                                component={CreateReviewPage}
                                authInfo={authStore.authInfo}
                            />
                            <PrivateRoute
                                path="/personal/:id"
                                component={PersonalPage}
                                authInfo={authStore.authInfo}
                            />
                            <PrivateRoute
                                path="/reviews"
                                component={Reviews}
                                authInfo={authStore.authInfo}
                            />
                            <PrivateRoute
                                path="/search-peoples"
                                component={SearchPeoplePage}
                                authInfo={authStore.authInfo}
                            />
                            <PrivateRoute
                                path="/search-structures"
                                component={SearchStructuresPage}
                                authInfo={authStore.authInfo}
                            />
                            <PrivateRoute
                                path="/add-survey"
                                component={AddSurveyPage}
                                authInfo={authStore.authInfo}
                            />
                        </Switch>
                    </Grid>
                </div>
            );
        } else {
            // Initial data is not loaded yet, show progress info
            return (<LinearProgress />);
        }
    }
}

export default App;
