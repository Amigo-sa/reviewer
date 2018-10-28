import { action, observable } from "mobx";
import PersonsApi from "src/server-api/persons/PersonsApi";
import { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";

export class SpecializationsStore {
    @observable
    public specializations: PersonSpecializationList[] = [];

    @action
    public get(id: string, force = false): Promise<PersonSpecializationList | undefined> {
        const user = this._peak(id);
        if (user && !force) {
            return Promise.resolve(user);
        }
        return PersonsApi.getPersonSpecializations(id)
            .then((a) => {
                if (a.result === 0 && a.list) {
                    // tslint:disable-next-line:no-shadowed-variable
                    const specializationList = new PersonSpecializationList();
                    specializationList.list = a.list;
                    this.specializations[id] = specializationList;
                    return specializationList;
                }
                return undefined;
            });
    }

    private _peak(id: string): PersonSpecializationList | undefined {
        const user = this.specializations[id];
        if (user) {
            return user;
        }
        return undefined;
    }

}

const specializationsStore = new SpecializationsStore();
export default specializationsStore;
