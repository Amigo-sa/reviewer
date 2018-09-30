import { IAuthorizationUIHelper } from "src/components/PrivateRoute";
import { AuthStore } from "src/stores/AuthStore";

/**
 * Implementation of authorization UI helper.
 */
export default class AuthorizationUIHelper implements IAuthorizationUIHelper {

    constructor(authStore: AuthStore) {
        this._authStore = authStore;
    }

    // Public methods

    public tryAuthenticate(): Promise<void> {
        return this._authStore.tryAuthenticate();
    }

    // Private fields

    private _authStore: AuthStore;
}
