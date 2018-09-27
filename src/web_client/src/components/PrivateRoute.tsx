import * as React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";
import { inject, observer } from "mobx-react";
import { REDIRECT_TO_LOGIN } from "../constants";
import { AuthStore } from "../stores/AuthStore";
import { ScaleLoader } from "react-spinners";

interface IAuthProps extends RouteProps {
  authStore: AuthStore;
}

interface IPrivateRoute {
  isAuth: boolean;
  pending: boolean;
}

@inject("authStore")
@observer
export default class PrivateRoute extends React.Component<RouteProps, IPrivateRoute> {
  constructor(props: RouteProps){
    super(props);
    this.state = {
      isAuth: false,
      pending: true,
    };
  }
  get injected() {
    return this.props as IAuthProps;
  }

  public componentDidMount() {
    const { authStore } = this.injected;
    authStore
      .tryAuthenticate()
      .then(() => this.setState({isAuth: true}))
      .catch(() => this.setState({isAuth: false}))
      .then(() => this.setState({pending: false}));
  }

  public render() {
    const Component: any = this.props.component;
    return (
        <Route
          render={ (props) => {
              if ( this.state.pending ) {
                return (
                  <div className={"Centered"}>
                    <ScaleLoader
                      height={150}
                      color={"#123abc"}
                      loading={this.state.pending}
                    />
                  </div>
                );
              }else {
                if ( !this.state.isAuth ){
                  return <Redirect to={REDIRECT_TO_LOGIN}/>;
                }
                // return React.createElement(Component, props)
                return <Component {...props}/>;
              }
            }
          }
        />
    );
  }
}
