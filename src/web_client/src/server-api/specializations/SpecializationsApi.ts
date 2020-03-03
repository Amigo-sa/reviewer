import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetSpecializationsListResponse from "./GetSpecializationsListResponse";

export default class SpecializationsApi {

    public static loadList(): Promise<GetSpecializationsListResponse> {
        return ServerApiHelper.makeGetRequest<GetSpecializationsListResponse>(null, SERVER_HOST + "/specializations");
    }

}
