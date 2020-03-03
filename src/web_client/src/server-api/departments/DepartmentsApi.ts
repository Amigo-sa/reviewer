import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetDepartmentsListResponse from "./GetDepartmentsListResponse";

export default class DepartmentsApi {

    public static loadList(organizationId: string): Promise<GetDepartmentsListResponse> {
        const url = SERVER_HOST + "/organizations/" + organizationId + "/departments";
        return ServerApiHelper.makeGetRequest<GetDepartmentsListResponse>(null, url);
    }

}
