import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetDepartmentsListResponce from "./GetDepartmentsListResponce";

export default class DepartmentsApi {

    public static loadList(organizationId: string): Promise<GetDepartmentsListResponce> {
        const url = SERVER_HOST + "/organizations/" + organizationId + "/departments";
        return ServerApiHelper.makeGetRequest<GetDepartmentsListResponce>(null, url);
    }

}
