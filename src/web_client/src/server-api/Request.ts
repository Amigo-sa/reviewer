/**
 * Base class of server-side requests.
 */
export default class Request {
    constructor(token: string) {
        this.authorizationToken = token;
    }

    public authorizationToken: string;
}
