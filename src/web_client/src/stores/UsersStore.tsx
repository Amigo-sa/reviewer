import { action, observable } from "mobx";
import PersonsApi from "src/server-api/persons/PersonsApi";
import Person from "src/server-api/persons/Person";
import GetPersonInfoResponse from "src/server-api/persons/GetPersonInfoResponse";

export class UsersStore {
    @observable
    public users: { [key: string]: Person } = {};

    public get(id: string, force = false): Promise<Person | undefined> {
        const user = this._peak(id);
        if (user && !force) {
            return Promise.resolve(user);
        }
        return PersonsApi.getPersonInfo(id)
            .then(action((response: GetPersonInfoResponse) => {
                if (response.result === 0 && response.data) {
                    this.users[id] = response.data;
                    return response.data;
                }
                return undefined;
            }));
    }

    private _peak(id: string): Person | undefined {
        const user = this.users[id];
        if (user) {
            return user;
        }
        return undefined;
    }

}

const usersStore = new UsersStore();
export default usersStore;
