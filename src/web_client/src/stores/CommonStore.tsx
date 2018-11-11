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
    public specializationList: Specialization[] = [];
    public softSkillList: Skill[] = [];
    public hardSkillList: Skill[] = [];

    public loadData(): Promise<any> {
        // Загрузка всех специализаций
        const loadSpecializations = SpecializationsApi.loadList()
            .then((result: GetSpecializationsListResponse) => {
                this.specializationList = result.list || [];
            });

        // Загрузка всех личностных характеристик
        const loadSoftSkills = SkillsApi.loadSoftSkillsList()
            .then((result: GetSkillsListResponse) => {
                this.softSkillList = result.list || [];
            });

        // Загрузка всех профессиональных навыков
        const loadHardSkills = SkillsApi.loadHardSkillsList()
            .then((result: GetSkillsListResponse) => {
                this.hardSkillList = result.list || [];
            });

        return Promise.all([loadSpecializations, loadSoftSkills, loadHardSkills]);
    }
}

const commonStore = new CommonStore();
export default commonStore;
