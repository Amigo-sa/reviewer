import { action, observable } from "mobx";
import PersonsApi from "src/server-api/persons/PersonsApi";
import Person from "src/server-api/persons/Person";

export class UsersStore {
    @observable
    public users: Person[] = [];

    @action
    public get(id: string, force = false): Promise<Person | undefined> {
        const user = this._peak(id);
        if (user && !force) {
            return Promise.resolve(user);
        }
        return PersonsApi.getPersonInfo(id)
            .then((a) => {
                if (a.result === 0) {
                    // tslint:disable-next-line:no-shadowed-variable
                    const user = a.data;
                    this.users[id] = user;
                    return user;
                }
                return undefined;
            });
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
