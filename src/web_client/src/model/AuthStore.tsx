import { action, observable } from "mobx";
import RegistrationApi from "src/server-api/registration/RegistrationApi";
import PersonsApi from "src/server-api/persons/PersonsApi";
import UserLoginRequest from "src/server-api/registration/UserLoginRequest";
import UserLoginResponse from "src/server-api/registration/UserLoginResponse";
import Person from "src/server-api/persons/Person";

// TODO: we really need only uid and token info
export interface IUserData {
    phone: string;
    token: string | undefined;
    uid?: string;
    data?: Person;
}

export class AuthStore {
    @observable public isAuth: boolean = false;

    @observable
    public user: IUserData = {
        phone: "",
        token: undefined,
        uid: undefined,
        data: undefined,
    };

    @observable
    public pending: boolean = false;

    constructor() {
        console.log("Construct AuthStore");
    }

    // TODO: do we need have it here?
    @action
    public setPhone(phone: string) {
        this.user.phone = phone;
    }

    // TODO: do we need have it here?
    @action public reset() {
        // this.user = null;
    }

    @action
    public authenticate(phone: string, password: string) {
        this.pending = true;
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
                this.pending = false;
            }))
            .catch((err) => {
                throw err;
                this.pending = true;
            });
    }

    @action public register() {
        console.log("Register");
    }

    @action public logout() {
        this.isAuth = false;
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
        this.pending = true;
        return this.getCurrentUser()
            .then(action(() => {
                this.isAuth = true;
                this.pending = false;
            }))
            .catch((err: object) => {
                this.isAuth = false;
                this.pending = false;
            });
    }

    private getCurrentUser(force?: boolean): Promise<IUserData> {
        let resultPromise: Promise<IUserData>;
        if (!force && this.user && this.isAuth) {
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
