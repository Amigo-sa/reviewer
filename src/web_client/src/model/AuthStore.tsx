import { action, observable } from "mobx";
import RegistrationApi from "src/server-api/registration/RegistrationApi";
import PersonsApi from "src/server-api/persons/PersonsApi";
import UserLoginRequest from "src/server-api/registration/UserLoginRequest";
import UserLoginResponse from "src/server-api/registration/UserLoginResponse";
import Person from "src/server-api/persons/Person";
import { AuthorizationInfo } from "src/components/PrivateRoute";

// TODO: we really need only uid and token info
export interface IUserData {
    token: string | undefined;
    uid?: string;
    data?: Person;
}

export class AuthStore {

    public authInfo: AuthorizationInfo = new AuthorizationInfo();

    @observable
    public user: IUserData = {
        token: undefined,
        uid: undefined,
        data: undefined,
    };

    @action
    public authenticate(phone: string, password: string) {
        return RegistrationApi.userLogin(new UserLoginRequest(phone, password))
            .then((responce: UserLoginResponse) => {
                this.setUser(responce);
            })
            .then(() => {
                this.getCurrentUser(true).catch((err) => {
                    console.error("get current user error", err);
                });
            })
            .then(action(() => {
                this.authInfo.isAuth = true;
            }))
            .catch((err) => {
                throw err;
            });
    }

    @action public register() {
        console.log("Register");
    }

    @action public logout() {
        this.authInfo.isAuth = false;
        localStorage.removeItem("User");
        return Promise.resolve();
    }

    @action
    private setUser(responce: UserLoginResponse) {
        this.user.uid = responce.person_id;
        this.user.token = responce.session_id;
        localStorage.setItem("User", JSON.stringify(this.user));
    }

    @action
    public tryAuthenticate() {
        return this.getCurrentUser()
            .then(action(() => {
                this.authInfo.isAuth = true;
            }))
            .catch((err: object) => {
                this.authInfo.isAuth = false;
            });
    }

    private getCurrentUser(force?: boolean): Promise<IUserData> {
        let resultPromise: Promise<IUserData>;
        if (!force && this.user && this.authInfo.isAuth) {
            resultPromise = Promise.resolve(this.user);
        }
        else {
            if (!this.user.uid && localStorage.getItem("User") != null) {
                this.user = JSON.parse(localStorage.getItem("User") || "");
            }
            if (this.user.uid) {
                resultPromise = new Promise<IUserData>((resolve, reject) => {
                    PersonsApi.getPersonInfo(this.user.uid!)
                        .then((result) => {
                            console.log("Load Person", result);
                            this.user.data = result.data;
                            resolve(this.user);
                        })
                        .catch((err) => {
                            // process error from server
                            reject(err);
                        });
                });
            }
            else {
                resultPromise = Promise.reject(new Error());
            }
        }

        return resultPromise;
    }
}

const authStore = new AuthStore();
export default authStore;
