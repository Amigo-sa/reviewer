import { action, observable } from "mobx";
import PersonsApi from "src/server-api/persons/PersonsApi";
import Person from "src/server-api/persons/Person";
import GetPersonInfoResponse from "src/server-api/persons/GetPersonInfoResponse";

export class PersonsStore {
    @observable
    public persons: { [key: string]: Person } = {};

    public get(id: string, force = false): Promise<Person | undefined> {
        const person = this._peak(id);
        if (person && !force) {
            return Promise.resolve(person);
        }
        return PersonsApi.getPersonInfo(id)
            .then(action((response: GetPersonInfoResponse) => {
                if (response.result === 0 && response.data) {
                    this.persons[id] = response.data;
                    return response.data;
                }
                return undefined;
            }));
    }

    private _peak(id: string): Person | undefined {
        const person = this.persons[id];
        if (person) {
            return person;
        }
        return undefined;
    }

}

const personsStore = new PersonsStore();
export default personsStore;
