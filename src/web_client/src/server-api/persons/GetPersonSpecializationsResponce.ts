import PersonSpecialization from "./PersonSpecialization";
import Response from "../Response";

export default class GetPersonsSpecializationsResponse extends Response {
    public list?: PersonSpecialization[];
}
