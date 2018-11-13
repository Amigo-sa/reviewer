import { observable, action, computed } from "mobx";
import Person from "src/server-api/persons/Person";
import { PersonSpecializationList } from "src/server-api/persons/PersonSpecialization";
import usersStore from "src/stores/UsersStore";
import PersonsApi from "src/server-api/persons/PersonsApi";
import FindPersonSoftSkillInfoResponse from "src/server-api/persons/FindPersonSoftSkillInfoResponse";
import FindPersonHardSkillInfoResponse from "src/server-api/persons/FindPersonHardSkillInfoResponse";
import HardSkill from "src/server-api/persons/HardSkill";
import commonStore from "src/stores/CommonStore";
import SoftSkill from "src/server-api/persons/SoftSkill";
import { DUMMY_AVATAR_URL } from "src/constants";
import FindPersonsRequest from "src/server-api/persons/FindPersonsRequest";
import FindPersonsResponse from "src/server-api/persons/FindPersonsResponse";

export default class PersonalInfoVM {

    // Constructor

    public constructor() {
        this.status = "Сотрудник";

        this.professionLists = [["менеджер", 8.5]];

        // tslint:disable-next-line:max-line-length
        this.personalNotes = "Возможно размещение короткого пояснительного текста о себе с указанием личных достижений и значимых наград Характер: спокойный, усидчивый, умение ставить цели и достигать их";
    }

    // Public properties

    @computed
    public get loaded(): boolean {
        return this._loaded;
    }

    public get specializationList(): PersonSpecializationList {
        return this._specializations;
    }

    @observable
    public personId: string;

    @observable
    public photoUrl: string;

    @observable
    public fullName: string;

    @observable
    public status: string;

    @observable
    public organizationName: string;

    @observable
    public hardSkills: HardSkillModel[];

    @observable
    public softSkills: SoftSkillModel[];

    @observable
    public professionLists: Array<[string, number]>;

    public personalNotes: string;

    // Public methods

    @action
    public loadPersonInfo(id: string): void {

        this._loaded = false;

        // Finds hard skills
        const findHardSkills = PersonsApi.findPersonHardSkills(id).then((result: FindPersonHardSkillInfoResponse) => {

            // Sort skills by rates
            const skills = result.list.sort((a: HardSkill, b: HardSkill) => {
                return b.level - a.level;
            });

            // Gets only needed piece of data
            this.hardSkills = new Array();
            skills.slice(0, PersonalInfoVM.SKILLS_COUNT_ON_PAGE).map((value) => {
                const skillName: string = commonStore.findHardSkillName(value.hs_id);
                this.hardSkills.push(new HardSkillModel(skillName, value.level));
            });
        });

        // Finds soft skills
        const findSoftSkills = PersonsApi.findPersonSoftSkills(id).then((result: FindPersonSoftSkillInfoResponse) => {

            // Sort skills by rates
            const skills = result.list.sort((a: SoftSkill, b: SoftSkill) => {
                return b.level - a.level;
            });

            // Gets only needed piece of data
            this.softSkills = new Array();
            skills.slice(0, PersonalInfoVM.SKILLS_COUNT_ON_PAGE).map((value) => {
                const skillName: string = commonStore.findSoftSkillName(value.ss_id);
                this.softSkills.push(new SoftSkillModel(skillName, value.level));
            });
        });

        // Load personal info
        const loadPersonInfo = usersStore.get(id).then((result: Person) => {
            this._updatePerson(result);
        });

        // TODO: test code for getting specializations
        // specializationsStore.get(id).then((result: PersonSpecializationList) => {
        //     this._specializations = result;
        //     this._loadingSpecializationFinish = true;

        //     // // update profession list
        //     // const professionLists = new Array(this._specializations.list.length);
        //     // for (let index = 0; index < professionLists.length; index++) {
        //     //     // const specialization = this._specializations.list[index];
        //     //     // const professionName = specialization.specialization_type;
        //     //     // const professionRate = specialization.level ? specialization.level : 100;

        //     //     // professionLists[index] = [professionName, professionRate];
        //     //     professionLists[index] = ["менеджер", 8.5];
        //     // }

        //     // this.professionLists = professionLists;
        // });

        // Wait all parallel tasks
        Promise.all([loadPersonInfo, findHardSkills, findSoftSkills]).then(() => {

            // TODO: temp get needed info over searching functionality
            const findPersonRequest = new FindPersonsRequest();
            findPersonRequest.first_name = this._person.first_name;
            findPersonRequest.middle_name = this._person.middle_name;
            findPersonRequest.surname = this._person.surname;
            PersonsApi.findPersons(findPersonRequest)
                .then((result: FindPersonsResponse) => {
                    this.organizationName = result.list![0].organization_name;
                    this.status = result.list![0].specialization_display_text!;

                    this._loaded = true;
                })
                .catch((err: any) => {
                    console.log("Error Search", err);
                    this._loaded = true;
                });

            // this._loaded = true;
        });
    }

    // Private methods

    private _updatePerson(person: Person) {
        this._person = person;

        this.personId = this._person.id;
        this.fullName = person.surname +
            " " + person.first_name +
            " " + person.middle_name;

        // Update photo url
        if (person.photo) {
            this.photoUrl = PersonsApi.personPhotoUrlById(this.personId);
        } else {
            this.photoUrl = DUMMY_AVATAR_URL;
        }
    }

    // Private constants

    private static SKILLS_COUNT_ON_PAGE: number = 4;

    // Private fields

    private _person: Person;

    @observable
    private _loaded: boolean;

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
