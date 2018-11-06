import { observable, action, computed } from "mobx";
import Person from "src/server-api/persons/Person";
import { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";
import specializationsStore from "src/stores/SpecializationsStore";
import usersStore from "src/stores/UsersStore";

export default class PersonalInfoVM {

    // Constructor

    public constructor() {
        this.fullName = "Пример";
        this.status = "Сотрудник";
        this.organizationName = "ИТМО";

        this.professionLists = [["менеджер", 8.5]];

        // tslint:disable-next-line:max-line-length
        this.personalNotes = "Возможно размещение короткого пояснительного текста о себе с указанием личных достижений и значимых наград Характер: спокойный, усидчивый, умение ставить цели и достигать их";

        this.hardSkills = [new HardSkillModel("целеустремленность", 90),
        new HardSkillModel("стрессоустойчивость", 79),
        new HardSkillModel("оперативность", 85),
        new HardSkillModel("готовность изучать новое", 60)];

        this.softSkills = [new SoftSkillModel("ответственность", 156),
        new SoftSkillModel("аккуратность", 85),
        new SoftSkillModel("организованость", 342)];
    }

    // Public properties

    @computed
    public get load(): boolean {
        return this._loadingPersonFinish && this._loadingSpecializationFinish;
    }

    public get specializationList(): PersonSpecializationList {
        return this._specializations;
    }

    @observable
    public personId: string;

    @observable
    public fullName: string;

    @observable
    public status: string;

    @observable
    public organizationName: string;

    @observable
    public professionLists: Array<[string, number]>;

    // Public methods

    @action
    public setupPerson(id: string): void {
        this._loadingPersonFinish = false;
        this._loadingSpecializationFinish = false;

        usersStore.get(id).then((result: Person) => {
            this._updatePerson(result);
            this._loadingPersonFinish = true;
        });

        specializationsStore.get(id).then((result: PersonSpecializationList) => {
            this._specializations = result;
            this._loadingSpecializationFinish = true;

            // // update profession list
            // const professionLists = new Array(this._specializations.list.length);
            // for (let index = 0; index < professionLists.length; index++) {
            //     // const specialization = this._specializations.list[index];
            //     // const professionName = specialization.specialization_type;
            //     // const professionRate = specialization.level ? specialization.level : 100;

            //     // professionLists[index] = [professionName, professionRate];
            //     professionLists[index] = ["менеджер", 8.5];
            // }

            // this.professionLists = professionLists;
        });
    }

    // Private methods

    private _updatePerson(person: Person) {
        this._person = person;

        this.personId = this._person.id;
        this.fullName = person.surname +
            " " + person.first_name +
            " " + person.middle_name;
    }

    // Private fields

    private _person: Person;

    public personalNotes: string;
    public hardSkills: HardSkillModel[];
    public softSkills: SoftSkillModel[];

    // DTO objects?

    @observable
    private _loadingPersonFinish: boolean;

    @observable
    private _loadingSpecializationFinish: boolean;

    private _specializations: PersonSpecializationList;
}

export class HardSkillModel {

    public constructor(name: string, value: number) {
        this.name = name;
        this.value = value;
    }

    public name: string;
    public value: number;
}

export class SoftSkillModel {
    public constructor(name: string, likesCount: number) {
        this.name = name;
        this.likesCount = likesCount;
    }

    public name: string;
    public likesCount: number;
}
