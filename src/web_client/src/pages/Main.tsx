import * as React from "react";
import RegistrationApi from "../server-api/registration/RegistrationApi";
import UserLoginRequest from "../server-api/registration/UserLoginRequest";
import UserLoginResponse from "../server-api/registration/UserLoginResponse";

class Main extends React.Component {
    public render() {

        RegistrationApi.userLogin(new UserLoginRequest("79032233223", "SomeSecurePass"))
            .then((response: UserLoginResponse) => {
                console.log(response.result);
                console.log(response.session_id);
            });

        return (
            "Main page"
        );
    }
}

export default Main;
