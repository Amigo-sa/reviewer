import Department from "./Department";
import Response from "../Response";

export default class GetDepartmentsListResponce extends Response {
    public list?: Department[];
}
