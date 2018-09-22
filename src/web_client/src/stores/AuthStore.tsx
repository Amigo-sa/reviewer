import { action, observable } from "mobx";
import auth from "../agent/auth";

interface IUserData {
    phone: string;
    password: string;
    token: string;
}

class AuthStore {

    constructor() {
        console.log("Construct AuthStore");
    }

    @action
    public setPhone(phone: string) {
        this.user.phone = phone;
    }

    @action public setPassword(password: string) {
        this.user.password = password;
    }

    @action public reset() {
        this.user.phone = "";
        this.user.password = "";
    }

    @action public login() {
        this.inProgress = true;
        this.errors = undefined;
        return auth.login(this.user.phone, this.user.password)
            .then((data) => {
                console.log(data);
                this.isAuth = true;
            }).catch(action((err) => {
                // this.errors = err.response && err.response.body && err.response.body.errors;
                console.log(err);
                throw err;
            }));
        // .finally(action(() => { this.inProgress = false; }));
    }

    @action public register() {
        console.log("Register");
    }

    @action public logout() {
        this.setToken("");
        return Promise.resolve();
    }
    @observable public inProgress: boolean = false;
    @observable public errors: any = undefined;
    @observable public isAuth: boolean = false;

    @observable
    public user: IUserData = {
        password: "",
        phone: "",
        token: "",
    };

    @action
    protected setToken(token: string) {
        this.user.token = token;
    }
}

export default new AuthStore();
