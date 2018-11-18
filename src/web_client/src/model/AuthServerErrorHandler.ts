import ErrorCodes from "src/server-api/ErrorCodes";
import application from "src/Application";

export default class AuthServerErrorHandler {

    public static handleError(errorCode: number): boolean {
        let result: boolean = false;

        // try to process authorization errors
        if (errorCode === ErrorCodes.TOKEN_EXPIRED) {
            application.showLoginDialog();
            result = true;
        }

        return result;
    }
}
