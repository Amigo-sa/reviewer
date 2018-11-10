import PersonalInfoVM from "./PersonalInfoVM";
import authStore from "src/stores/AuthStore"; // TODO: get auth store from constructor
import { observable, computed, action } from "mobx";
import { ReviewsVM } from "./ReviewsVM";

/**
 * Personal page view model.
 * It contains all needed data for personal page.
 */
export default class PersonalPageVM {

    // Constructor

    public constructor() {
        // accept abstractions which help to get needed data for UI
        this._personalInfoVM = new PersonalInfoVM();
        this._reviewsVM = new ReviewsVM();
    }

    // Public properties

    public get personId(): string {
        return this._personId;
    }

    public get personalInfoVM() {
        return this._personalInfoVM;
    }

    public get reviewsVM() {
        return this._reviewsVM;
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
            this.isCurrentPerson = true;
        }
        this._personalInfoVM.setupPerson(this._personId);
    }

    // Private fields

    private _personalInfoVM: PersonalInfoVM;
    private _personId: string;
    private _reviewsVM: ReviewsVM;
}