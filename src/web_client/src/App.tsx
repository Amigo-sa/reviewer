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
import commonStore from "./stores/CommonStore";
import CommonUIHelper from "./CommonUIHelper";
import Reviews from "./pages/ReviewPage";
import CreateReviewPage from "./pages/ReviewPage/CreateReviewPage";

const authUIHelper = new AuthorizationUIHelper(authStore);
const commonUIHelper = new CommonUIHelper(commonStore);

class App extends React.Component<any> {

    public componentWillMount() {
        // TODO: а если это займет много времени, как пользователя будет оповещать об этом?
        commonUIHelper.tryLoadData();
    }

    public render() {
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
                        <Route
                            exact
                            path="/personal"
                            component={PersonalPage}
                            authHelper={authUIHelper}
                        />
                        {/* TODO необходимо переносить роуты внутрь управляющих страниц! */}
                        <Route
                            exact
                            path="/personal/:id/review"
                            component={CreateReviewPage}
                            authHelper={authUIHelper}
                        />
                        <Route
                            path="/personal/:id/review/:specid"
                            component={CreateReviewPage}
                            authHelper={authUIHelper}
                        />
                        <Route
                            path="/personal/:id"
                            component={PersonalPage}
                            authHelper={authUIHelper}
                        />
                        <Route
                            path="/reviews"
                            component={Reviews}
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
