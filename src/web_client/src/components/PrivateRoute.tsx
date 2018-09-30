import * as React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";
import { REDIRECT_TO_LOGIN } from "../constants";
import { ScaleLoader } from "react-spinners";

/**
 * Interface of authorizaiton helper.
 * Knows how to work with authorization in application.
 */
export interface IAuthorizationUIHelper {
    tryAuthenticate(): Promise<void>;
}

interface IPrivateRouteProps extends RouteProps {
    authHelper: IAuthorizationUIHelper;
}

interface IPrivateRouteState {
    isAuth: boolean;
    pending: boolean;
}

/**
 * PrivateRoute component.
 * Helps to work with private pages.
 */
export default class PrivateRoute extends React.Component<IPrivateRouteProps, IPrivateRouteState> {
    constructor(props: IPrivateRouteProps) {
        super(props);
        this.state = {
            isAuth: false,
            pending: true,
        };
    }

    public componentDidMount() {
        // check if user already make authorization
        // TODO: make checking

        // try to authorization
        this.props.authHelper
            .tryAuthenticate()
            .then(() => this.setState({ isAuth: true }))
            .catch(() => this.setState({ isAuth: false }))
            .then(() => this.setState({ pending: false }));
    }

    public render() {
        const Component: any = this.props.component;
        return (
            <Route
                render={(props) => {
                    if (this.state.pending) {
                        return (
                            <div className={"Centered"}>
                                <ScaleLoader
                                    height={150}
                                    color={"#123abc"}
                                    loading={this.state.pending}
                                />
                            </div>
                        );
                    } else {
                        if (!this.state.isAuth) {
                            // TODO: need to add info about from where we open Login page.
                            // We need to redirect to this page after user makes logining success
                            return <Redirect to={REDIRECT_TO_LOGIN} />;
                        }
                        return <Component {...props} />;
                    }
                }
                }
            />
        );
    }
}
