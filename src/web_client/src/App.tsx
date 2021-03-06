import * as React from "react";
import { Route, Switch, withRouter, RouteComponentProps, Redirect } from "react-router";
import "./App.css";
import AddSurveyPage from "./pages/AddSurveyPage";
import Main from "./pages/MainPage/Main";
import PersonalPage from "./pages/PersonalPage";
import SearchPeoplePage from "./pages/SearchPeoplePage";
import SearchStructuresPage from "./pages/SearchStructuresPage";
import PrivateRoute from "./components/PrivateRoute";
import LoginPage from "./pages/LoginPage";
import Grid from "@material-ui/core/Grid";
import Reviews from "./pages/ReviewPage";
import CreateReviewPage from "./pages/ReviewPage/CreateReviewPage";
import { LinearProgress, Dialog, Snackbar } from "@material-ui/core";
import application from "./Application";
import AppVM, { IAppVMListener } from "./AppVM";
import LoginDialog from "./pages/components/LoginDialog";

// TODO: we have to use VM + listener approach instead of mobx, because @observer
// decarator blocks updating of routes
class App extends React.Component<RouteComponentProps<{}>> implements IAppVMListener {

    constructor(props: any) {
        super(props);
        // attach to view model as listener
        this._appVM.attachListener(this);
    }

    // Implements of IViewModelListener

    public onUpdate(): void {
        // redraw react component
        this.forceUpdate();
    }

    public componentDidMount() {
        this._appVM.initilalLoad();
    }

    public render() {
        if (this._appVM.loaded) {
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
                            />
                            {/* TODO необходимо переносить роуты внутрь управляющих страниц! */}
                            {/* TODO: why do we use review url for current person? */}
                            <PrivateRoute
                                exact
                                path="/personal/:id/review"
                                component={CreateReviewPage}
                            />
                            <PrivateRoute
                                path="/personal/:id/review/:specid"
                                component={CreateReviewPage}
                            />
                            <PrivateRoute
                                path="/personal/:id"
                                component={PersonalPage}
                            />
                            <PrivateRoute
                                path="/reviews"
                                component={Reviews}
                            />
                            <PrivateRoute
                                path="/search-peoples"
                                component={SearchPeoplePage}
                            />
                            <PrivateRoute
                                path="/search-structures"
                                component={SearchStructuresPage}
                            />
                            <PrivateRoute
                                path="/add-survey"
                                component={AddSurveyPage}
                            />
                        </Switch>
                    </Grid>
                    {this._showLoginDialog()}
                    {this._goPrevLocationOnAuth()}
                    {this._showError()}
                </div>
            );
        } else {
            // Initial data is not loaded yet, show progress info
            return (<LinearProgress />);
        }
    }

    // Private methods

    /**
     * Shows error.
     */
    private _showError() {
        if (this._appVM.isErrorShown) {
            return (
                <Snackbar
                    anchorOrigin={{
                        vertical: "bottom",
                        horizontal: "left",
                    }}
                    open
                    onClose={() => this._appVM.hideError()}
                    autoHideDuration={5000}
                    message={this._appVM.errorMessage}
                />
            );
        } else {
            return null;
        }
    }

    private _showLoginDialog() {
        if (this._appVM.isLoginDialogShown) {
            return (
                <Dialog
                    open
                    aria-labelledby="form-dialog-title"
                    onClose={() => this._appVM.hideLoginDialog()}
                >
                    <LoginDialog
                        handleAuthClose={() => {
                            this._appVM.isAuth = true;
                            this._appVM.hideLoginDialog();
                        }}
                    />
                </Dialog>
            );
        } else {
            return null;
        }

    }

    private _goPrevLocationOnAuth() {
        if (this._appVM.prevLocation && this._appVM.isAuth) {
            const prevLocation = this._appVM.prevLocation;
            console.log("Go to", prevLocation);
            this._appVM.removePrevLocation();
            return <Redirect to={prevLocation} />;
        } else {
            return null;
        }
    }

    private _appVM: AppVM = application.appVM;
}

export default withRouter(App);
