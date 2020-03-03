import Department from "./Department";
import Response from "../Response";

export default class GetDepartmentsListResponse extends Response {
    public list?: Department[];
}
