import { action, observable } from "mobx";
import auth from "../agent/auth";
import UserLoginResponse from "../server-api/registration/UserLoginResponse";
import ErrorCodes from "../server-api/ErrorCodes";
import { rejects } from "assert";

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
        return auth.login(phone, password)
            .then((responce: UserLoginResponse) => { this.setUser(responce); })
            .then(() => { this.getCurrentUser(true); })
            .then(action(() => { this.setPhone(phone); this.isAuth = true; }))
            .catch(( err ) => { console.error("Authenticate", err); });
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
        this.user.session_id = token;
    }

    @action
    public tryAuthenticate() {
        return this.getCurrentUser()
            .then(action(() => { this.isAuth = true; }))
            .catch((err: object) => { console.error("tryAuthenticate", err); });
    }

    protected getCurrentUser(force?: boolean): Promise<Response> {
        return !force && this.user && this.isAuth
            ? Promise.resolve(this.user)
            : auth.get(this.user);
    }
}

export const authStore = new AuthStore();
