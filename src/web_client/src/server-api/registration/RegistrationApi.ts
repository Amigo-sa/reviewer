import UserLoginRequest from "./UserLoginRequest";
import UserLoginResponse from "./UserLoginResponse";
import ServerApiHelper from "../ServerApiHelper";
import { SERVER_HOST } from "src/constants";
import UserProfileResponce from "./UserProfileResponce";

export default class RegistrationApi {

    public static userLogin(request: UserLoginRequest): Promise<UserLoginResponse> {
        return ServerApiHelper.makePostRequest<UserLoginResponse>(request, SERVER_HOST + "/user_login");
    }

    // TODO: move to Persons class
    public static getProfile(uid: string): Promise<UserProfileResponce> {
        return ServerApiHelper.makeGetRequest<UserProfileResponce>(null, SERVER_HOST + "/persons/" + uid, true);
    }

    // TODO: move to Persons model
    public static getAllProfiles(): Promise<UserProfileResponce> {
        return ServerApiHelper.makeGetRequest<UserProfileResponce>(null, SERVER_HOST + "/persons", true);
    }
}
