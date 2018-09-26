import * as React from "react";
import { Route, Redirect, RouteProps } from "react-router-dom";
import { inject, observer } from "mobx-react";
import { REDIRECT_TO } from "../constants";
import { AuthStore } from "../stores/AuthStore";
import { RouterProps } from "react-router";
import { Component } from "react";

interface IAuthProps extends RouteProps {
    auth: AuthStore;
}

@inject("auth")
@observer
export default class PrivateRoute extends React.Component<RouteProps, {}> {
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
    let { auth } = this.injected;
    auth
      .tryAuthenticate()
      .then(() => this.setState({isAuth: true}))
      .catch(() => this.setState({isAuth: false}))
      .then(() => this.setState({pending: false}));
  }

  public render() {
    let Comp = this.props.component;
    const { auth } = this.injected;
    return <Route render={ props => {
              if(this.state.pending) {
                return (
                  <div className={'Centered'}>
                    <Spinner name="tree-bounce" color="blue"/> 
                  </div>
                )
              }else {
                if(!this.state.isAuth){
                  return <Redirect to={REDIRECT_TO}/>
                }
                return <Comp {...props}/>
              }
            }} />
  }
}
