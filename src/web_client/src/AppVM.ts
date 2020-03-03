import commonStore from "./model/CommonStore";
import authStore from "./model/AuthStore";

export interface IAppVMListener {
    /**
     * Gets notification about changes of inner state of view model.
     */
    onUpdate(): void;
}

export default class AppVM {

    // Public properties

    public loaded: boolean = false;
    public isAuth: boolean = false;

    public isErrorShown: boolean = false;

    public errorMessage?: string;

    // Public methods

    /**
     * Attaches listener to view mdoel.
     * @param listener Instance of view model listener.
     */
    public attachListener(listener: IAppVMListener): void {
        this._listener = listener;
    }

    /**
     * Detaches listener from view model.
     */
    public detachListener(): void {
        this._listener = null;
    }

    public initilalLoad(): void {
        this.loaded = false;
        this._notifyListener();

        const loadCommonData = commonStore.loadData();
        const tryAuthorizate = authStore.tryAuthenticate();

        Promise.all([loadCommonData, tryAuthorizate]).then(() => {
            this.loaded = true;
            this._notifyListener();
        },
            () => {
                console.error("Inital loading error");
            });
    }

    public showError(errorMessage: string): void {
        this.isErrorShown = true;
        this.errorMessage = errorMessage;
        this._notifyListener();
    }

    public hideError(): void {
        this.isErrorShown = false;
        this.errorMessage = undefined;
        this._notifyListener();
    }

    public isLoginDialogShown: boolean = false;

    public showLoginDialog(): void {
        this.isLoginDialogShown = true;
        this._notifyListener();
    }

    public hideLoginDialog(): void {
        this.isLoginDialogShown = false;
        this._notifyListener();
    }

    public prevLocation: string | null = null;

    public setPrevLocation(location: string): void {
        this.prevLocation = location;
        this._notifyListener();

    }

    public removePrevLocation(): void {
        this.prevLocation = null;
        this._notifyListener();

    }
    // Private methods

    /**
     * Notifies listener about inner changes.
     */
    private _notifyListener() {
        if (this._listener !== null) {
            this._listener.onUpdate();
        }
    }

    // Private fields

    // listener of view model changes
    private _listener: IAppVMListener | null;
}
