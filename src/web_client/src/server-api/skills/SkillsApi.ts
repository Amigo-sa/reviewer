import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetSkillsListResponce from "./GetSkillsListResponce";

export default class SkillsApi {

    public static loadSoftSkillsList(): Promise<GetSkillsListResponce> {
        return ServerApiHelper.makeGetRequest<GetSkillsListResponce>(null, SERVER_HOST + "/soft_skills");
    }

    public static loadHardSkillsList(): Promise<GetSkillsListResponce> {
        return ServerApiHelper.makeGetRequest<GetSkillsListResponce>(null, SERVER_HOST + "/hard_skills");
    }

}
