import Skill from "./Skill";
import Response from "../Response";

export default class GetSkillsListResponse extends Response {
    public list?: Skill[];
}
