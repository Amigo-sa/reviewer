import RegistrationApi from "../server-api/registration/RegistrationApi";
import UserLoginRequest from "../server-api/registration/UserLoginRequest";
import ErrorCodes from "../server-api/ErrorCodes";
import { IUserData } from "../stores/AuthStore";

const auth = {
    login: (phone: string, password: string) => {
        return RegistrationApi.userLogin(new UserLoginRequest(phone, password));
    },

    get: ( user?: IUserData) => {
        if ( user && user.session_id && user.uid ) {
            // TODO send request to get user
            const headers = new Object();
            headers["Authorization"] = "Bearer " + user.session_id;
            RegistrationApi.getAllProfiles(headers).then((data) => { console.log("Persons", data); });

            const me = RegistrationApi.getProfile(headers, user.uid).then((data) => { console.log("Person", data); });
            console.log("Person", me);
            return Promise.resolve("Ура получили данные");
        }
        else {
            return Promise.reject(ErrorCodes.AUTHORIZATION_ERROR);
        }
    },
};

export default auth;
