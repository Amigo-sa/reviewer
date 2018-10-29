import { observable, action } from "mobx";
import Specialization from "../server-api/specializations/Specialization";
import SpecializationsApi from "../server-api/specializations/SpecializationsApi";
import GetSpecializationsListResponse from "../server-api/specializations/GetSpecializationsListResponse";
import Skill from "../server-api/skills/Skill";
import SkillsApi from "../server-api/skills/SkillsApi";
import GetSkillsListResponse from "src/server-api/skills/GetSkillsListResponse";

/*
** CommonStore
** content lists of all common date from server
*/

export class CommonStore {
    @observable
    public specializationList: Specialization[] = [];
    @observable
    public softSkillList: Skill[] = [];
    @observable
    public hardSkillList: Skill[] = [];

    constructor() {
        console.debug("Construct CommonStore");
    }

    @action
    public loadData() {
        // Загрузка всех специализаций
        SpecializationsApi.loadList()
            .then(action((result: GetSpecializationsListResponse) => {
                this.specializationList = result.list || [];
            }));

        // Загрузка всех личностных характеристик
        SkillsApi.loadSoftSkillsList()
            .then(action((result: GetSkillsListResponse) => {
                this.softSkillList = result.list || [];
            }));

        // Загрузка всех профессиональных навыков
        SkillsApi.loadHardSkillsList()
            .then(action((result: GetSkillsListResponse) => {
                this.hardSkillList = result.list || [];
            }));
    }
}

const commonStore = new CommonStore();
export default commonStore;
