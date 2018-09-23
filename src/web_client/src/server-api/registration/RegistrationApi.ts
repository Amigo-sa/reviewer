import UserLoginRequest from "./UserLoginRequest";
import UserLoginResponse from "./UserLoginResponse";
import ServerApiHelper from "../ServerApiHelper";
import { SERVER_HOST } from "src/constants";

export default class RegistrationApi {

    public static userLogin(request: UserLoginRequest): Promise<UserLoginResponse> {
        return ServerApiHelper.makePostRequest<UserLoginResponse>(request,
            SERVER_HOST + "/user_login");
    }
}
