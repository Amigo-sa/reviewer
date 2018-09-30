import { action, observable } from "mobx";
import RegistrationApi from "src/server-api/registration/RegistrationApi";
import PersonsApi from "src/server-api/persons/PersonsApi";
import UserLoginRequest from "src/server-api/registration/UserLoginRequest";
import UserLoginResponse from "../server-api/registration/UserLoginResponse";

export interface IUserData {
    phone: string;
    session_id?: string;
    uid?: string;
    data?: object;
}

export class AuthStore {
    @observable public isAuth: boolean = false;

    @observable
    public user: IUserData = {
        phone: "",
        session_id: undefined,
        uid: undefined,
        data: undefined,
    };

    constructor() {
        console.log("Construct AuthStore");
    }

    @action
    public setPhone(phone: string) {
        this.user.phone = phone;
    }

    @action public reset() {
        // this.user = null;
    }

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
                this.setPhone(phone);
                this.isAuth = true;
            }))
            .catch((err) => {
                console.error("Authenticate", err);
            });
    }

    @action public register() {
        console.log("Register");
    }

    @action public logout() {
        this.setToken("");
        return Promise.resolve();
    }

    @action
    protected setUser(responce: UserLoginResponse) {
        this.setToken(responce.session_id);
        this.user.uid = responce.person_id;
    }

    @action
    protected setToken(token?: string) {
        localStorage.setItem("Token", JSON.stringify(token));
        this.user.session_id = token;
    }

    @action
    public tryAuthenticate() {
        return this.getCurrentUser()
            .then(action(() => { this.isAuth = true; }))
            .catch((err: object) => { console.error("Authenticate false"); throw err; });
    }

    private getCurrentUser(force?: boolean): Promise<IUserData> {
        let resultPromise: Promise<IUserData>;

        if (!force && this.user && this.isAuth && this.user.session_id) {
            resultPromise = Promise.resolve(this.user);
        }
        else {
            if (this.user.uid) {
                resultPromise = new Promise<IUserData>((resolve, reject) => {
                    PersonsApi.getPersonInfo(this.user.uid!)
                        .then((data) => {
                            console.log("Person", data);
                            resolve(this.user);
                        })
                        .catch((err) => {
                            // process error from server
                            resolve(err);
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
