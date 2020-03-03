import Specialization from "./Specialization";
import Response from "../Response";

export default class GetSpecializationsListResponse extends Response {
    public list?: Specialization[];
}
