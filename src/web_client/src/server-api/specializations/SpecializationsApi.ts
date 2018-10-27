import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetSpecializationsListResponce from "./GetSpecializationsListResponce";

export default class SpecializationsApi {

    public static loadList(): Promise<GetSpecializationsListResponce> {
        return ServerApiHelper.makeGetRequest<GetSpecializationsListResponce>(null, SERVER_HOST + "/specializations");
    }

}
