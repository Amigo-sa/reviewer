import { action, observable } from "mobx";
import PersonsApi from "src/server-api/persons/PersonsApi";
import { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";
import GetPersonsSpecializationsResponse from "src/server-api/persons/GetPersonSpecializationsResponse";

export class SpecializationsStore {
    @observable
    public specializations: { [key: string]: PersonSpecializationList } = {};

    @action
    public get(id: string, force = false): Promise<PersonSpecializationList | undefined> {
        const specialization = this._peak(id);
        if (specialization && !force) {
            return Promise.resolve(specialization);
        }
        return PersonsApi.getPersonSpecializations(id)
            .then((response: GetPersonsSpecializationsResponse) => {
                if (response.result === 0 && response.list) {
                    const specializationList = new PersonSpecializationList();
                    specializationList.list = response.list;
                    this.specializations[id] = specializationList;
                    return specializationList;
                }
                return undefined;
            });
    }

    private _peak(id: string): PersonSpecializationList | undefined {
        const specialization = this.specializations[id];
        if (specialization) {
            return specialization;
        }
        return undefined;
    }

}

const specializationsStore = new SpecializationsStore();
export default specializationsStore;
