import UserLoginRequest from "./UserLoginRequest";
import UserLoginResponse from "./UserLoginResponse";
import ServerApiHelper from "../ServerApiHelper";
import { SERVER_HOST } from "src/constants";
import UserProfileResponce from "./UserProfileResponce";

export default class RegistrationApi {

    public static userLogin(request: UserLoginRequest): Promise<UserLoginResponse> {
        return ServerApiHelper.makePostRequest<UserLoginResponse>(SERVER_HOST + "/user_login", { request });
    }

    // TODO: move to Persons class
    public static getProfile(headers: object, uid: string): Promise<UserProfileResponce> {
        return ServerApiHelper.makeGetRequest<UserProfileResponce>(SERVER_HOST + "/persons/" + uid, {headers});
    }

    // TODO: move to Persons model
    public static getAllProfiles(headers: object): Promise<UserProfileResponce> {
        return ServerApiHelper.makeGetRequest<UserProfileResponce>(SERVER_HOST + "/persons", {headers});
    }
}
