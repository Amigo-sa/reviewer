import { observable, action } from "mobx";
import Specialization from "../server-api/specializations/Specialization";
import SpecializationsApi from "../server-api/specializations/SpecializationsApi";
import GetSpecializationsListResponce from "../server-api/specializations/GetSpecializationsListResponce";
import Skill from "../server-api/skills/Skill";
import SkillsApi from "..//server-api/skills/SkillsApi";
import GetSkillsListResponce from "src/server-api/skills/GetSkillsListResponce";

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
            .then(action((result: GetSpecializationsListResponce) => {
                this.specializationList = result.list || [];
            }));

        // Загрузка всех личностных характеристик
        SkillsApi.loadSoftSkillsList()
            .then(action((result: GetSkillsListResponce) => {
                this.softSkillList = result.list || [];
            }));

        // Загрузка всех профессиональных навыков
        SkillsApi.loadHardSkillsList()
            .then(action((result: GetSkillsListResponce) => {
                this.hardSkillList = result.list || [];
            }));
    }
}

const commonStore = new CommonStore();
export default commonStore;
