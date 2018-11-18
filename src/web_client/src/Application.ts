import AppVM from "src/AppVM";

class Application {

    public get appVM(): AppVM {
        return this._appVM;
    }

    // Private fields

    private _appVM: AppVM = new AppVM();
}

const application = new Application();
export default application;
