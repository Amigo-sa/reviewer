import Specialization from "../server-api/specializations/Specialization";
import SpecializationsApi from "../server-api/specializations/SpecializationsApi";
import GetSpecializationsListResponse from "../server-api/specializations/GetSpecializationsListResponse";
import Skill from "../server-api/skills/Skill";
import SkillsApi from "../server-api/skills/SkillsApi";
import GetSkillsListResponse from "src/server-api/skills/GetSkillsListResponse";

/*
** CommonStore class.
** It contans all common data from server
*/
export class CommonStore {
    public specializationList: Specialization[] = [];

    /**
     * Loads all needed common data from server.
     */
    public loadData(): Promise<any> {
        // Загрузка всех специализаций
        const loadSpecializations = SpecializationsApi.loadList()
            .then((result: GetSpecializationsListResponse) => {
                this.specializationList = result.list || [];
            });

        // Загрузка всех личностных характеристик
        const loadSoftSkills = SkillsApi.loadSoftSkillsList()
            .then((result: GetSkillsListResponse) => {
                this._softSkillList = result.list || [];
            });

        // Загрузка всех профессиональных навыков
        const loadHardSkills = SkillsApi.loadHardSkillsList()
            .then((result: GetSkillsListResponse) => {
                this._hardSkillList = result.list || [];
            });

        return Promise.all([loadSpecializations, loadSoftSkills, loadHardSkills]);
    }

    /**
     * Finds hard skill name by its id.
     * @param skillId id of skill.
     * @return name of skill.
     */
    public findHardSkillName(skillId: string): string {
        const skill: Skill | undefined = this._hardSkillList.find((value) => {
            return value.id === skillId;
        });
        // TODO: add assertion
        if (skill) {
            return skill.name;
        }
        else {
            return "";
        }
    }

    /**
     * Finds soft skill name by its id.
     * @param skillId id of skill.
     * @return name of skill.
     */
    public findSoftSkillName(skillId: string): string {
        const skill: Skill | undefined = this._softSkillList.find((value) => {
            return value.id === skillId;
        });
        // TODO: add assertion
        if (skill) {
            return skill.name;
        }
        else {
            return "";
        }
    }

    // Private fields

    // Stores all available hard skills
    private _hardSkillList: Skill[] = [];
    // Stores all available soft skills
    private _softSkillList: Skill[] = [];
}

// export singleton instance of class.
const commonStore = new CommonStore();
export default commonStore;
