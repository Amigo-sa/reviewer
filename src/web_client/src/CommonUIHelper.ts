
import { CommonStore } from "src/stores/CommonStore";
/**
 * Implementation of common UI helper.
 */
export default class CommonUIHelper {

    constructor(commonStore: CommonStore) {
        this._commonStore = commonStore;
    }

    // Public methods

    public tryLoadData(): void {
        this._commonStore.loadData();
    }

    // Private fields

    private _commonStore: CommonStore;
}
