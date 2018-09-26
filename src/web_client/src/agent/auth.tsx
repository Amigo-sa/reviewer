import RegistrationApi from "../server-api/registration/RegistrationApi";
import UserLoginRequest from "../server-api/registration/UserLoginRequest";
import Request from "../server-api/Request";
import ErrorCodes from "../server-api/ErrorCodes";
import { IUserData } from "../stores/AuthStore";

const auth = {
    login: (phone: string, password: string) => {
        return RegistrationApi.userLogin(new UserLoginRequest(phone, password));
    },

    get: ( user?: IUserData) => {
        if ( user && user.session_id && user.uid ) {
            // TODO send request to get user
            return RegistrationApi.getProfile(new Request( user.session_id ), user.uid);
        }
        else {
            return Promise.reject(ErrorCodes.AUTHORIZATION_ERROR);
        }
    },
};

export default auth;
