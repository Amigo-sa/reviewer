import Response from "src/server-api/Response";

export default class UserLoginResponse extends Response {
    // tslint:disable-next-line:variable-name
    public person_id?: string;
    // tslint:disable-next-line:variable-name
    public session_id?: string;
}
