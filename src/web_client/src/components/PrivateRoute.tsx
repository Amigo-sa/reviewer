import * as React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";
import { REDIRECT_TO_LOGIN } from "src/constants";
import { observer } from "mobx-react";
import { observable } from "mobx";

export class AuthorizationInfo {
    @observable
    public isAuth: boolean = false;
}

interface IProps extends RouteProps {
    authInfo: AuthorizationInfo;
}

/**
 * PrivateRoute component.
 * Helps to work with private pages.
 */
@observer
export default class PrivateRoute extends React.Component<IProps> {

    public render() {
        const routeProps = {
            location: this.props.location,
            children: this.props.children,
            path: this.props.path,
            exact: this.props.exact,
            sensitive: this.props.sensitive,
            strict: this.props.strict,
        };

        if (!this.props.authInfo.isAuth) {
            // TODO: need to add info about from where we open Login page.
            // We need to redirect to this page after user makes logining success
            return <Redirect to={REDIRECT_TO_LOGIN} />;
        } else {
            const Component: any = this.props.component;
            return (
                <Route
                    {...routeProps}
                    render={(props) => <Component {...props} />}
                />
            );
        }
    }
}
