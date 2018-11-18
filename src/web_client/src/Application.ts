import AppVM from "src/AppVM";

class Application {

    // Public properties

    public get appVM(): AppVM {
        return this._appVM;
    }

    // Public methods

    public showError(errorMessage: string): void {
        this._appVM.showError(errorMessage);
    }

    // Private fields

    private _appVM: AppVM = new AppVM();
}

const application = new Application();
export default application;
