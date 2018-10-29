import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetSkillsListResponse from "./GetSkillsListResponse";

export default class SkillsApi {

    public static loadSoftSkillsList(): Promise<GetSkillsListResponse> {
        return ServerApiHelper.makeGetRequest<GetSkillsListResponse>(null, SERVER_HOST + "/soft_skills");
    }

    public static loadHardSkillsList(): Promise<GetSkillsListResponse> {
        return ServerApiHelper.makeGetRequest<GetSkillsListResponse>(null, SERVER_HOST + "/hard_skills");
    }

}
