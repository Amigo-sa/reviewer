export default class UserLoginRequest {
    public constructor(phone: string, password: string) {
        this.phone_no = phone;
        this.password = password;
    }

    // tslint:disable-next-line:variable-name
    public phone_no: string;
    public password: string;
}
