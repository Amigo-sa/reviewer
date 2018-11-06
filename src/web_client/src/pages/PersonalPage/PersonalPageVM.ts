import PersonalInfoVM from "./PersonalInfoVM";
import authStore from "src/stores/AuthStore"; // TODO: get auth store from constructor
import { observable, computed, action } from "mobx";

/**
 * Personal page view model.
 * It contains all needed data for personal page.
 */
export default class PersonalPageVM {

    // Constructor

    public constructor() {
        // accept abstractions which help to get needed data for UI
        this._personalInfoVM = new PersonalInfoVM();
    }

    // Public properties

    public get personId(): string {
        return this._personId;
    }

    public get personalInfoVM() {
        return this._personalInfoVM;
    }

    /**
     * Indicates if all needed data is loaded.
     */
    @computed
    public get loaded(): boolean {
        return this._personalInfoVM.load;
    }

    @observable
    public isCurrentPerson: boolean;

    // Public methods

    @action
    public setupPerson(id: string | null): void {
        if (id) {
            this._personId = id;
            this.isCurrentPerson = false;
        }
        else {
            // id is null, so we would like to show personal page for current user
            this._personId = authStore.user.uid!;
            this.isCurrentPerson = false;
        }
        this._personalInfoVM.setupPerson(this._personId);
    }

    // Private fields

    private _personalInfoVM: PersonalInfoVM;
    private _personId: string;
}
