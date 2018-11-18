import Person from "src/server-api/persons/Person";
import AddPersonResponse from "./AddPersonResponse";
import ServerApiHelper from "../ServerApiHelper";
import { SERVER_HOST } from "src/constants";
import FindPersonsRequest from "./FindPersonsRequest";
import FindPersonsResponse from "./FindPersonsResponse";
import Response from "../Response";
import GetPersonInfoResponse from "./GetPersonInfoResponse";
import GetPersonsSpecializationsResponse from "./GetPersonSpecializationsResponse";
import FindPersonHardSkillInfoResponse from "./FindPersonHardSkillInfoResponse";
import FindPersonSoftSkillInfoResponse from "./FindPersonSoftSkillInfoResponse";

export default class PersonsApi {

    public static personPhotoUrlById(id: string | undefined): string {
        if (id) {
            return SERVER_HOST + "/persons/" + id + "/photo";
        }
        else {
            return "";
        }
    }

    public static addPerson(person: Person): Promise<AddPersonResponse> {
        return ServerApiHelper.makePostRequest<AddPersonResponse>(person, SERVER_HOST + "/persons", true);
    }

    public static findPersons(request: FindPersonsRequest): Promise<FindPersonsResponse> {
        return ServerApiHelper.makeGetRequest<FindPersonsResponse>(request, SERVER_HOST + "/persons");
    }

    public static deletePerson(personId: string): Promise<Response> {
        const url = SERVER_HOST + "/persons/" + personId;
        return ServerApiHelper.makeDeleteRequest<Response>(null, url, true);
    }

    public static getPersonInfo(personId: string): Promise<GetPersonInfoResponse> {
        const url = SERVER_HOST + "/persons/" + personId;
        return ServerApiHelper.makeGetRequest<GetPersonInfoResponse>(null, url, true);
    }

    public static getPersonSpecializations(personId: string): Promise<GetPersonsSpecializationsResponse> {
        const url = SERVER_HOST + "/persons/" + personId + "/specializations";
        return ServerApiHelper.makeGetRequest<GetPersonsSpecializationsResponse>(null, url);
    }

    public static findPersonSoftSkills(personId: string): Promise<FindPersonSoftSkillInfoResponse> {
        const url = SERVER_HOST + "/persons/soft_skills";
        return ServerApiHelper.makeGetRequest<FindPersonSoftSkillInfoResponse>({ person_id: personId }, url);
    }

    public static findPersonHardSkills(personId: string): Promise<FindPersonHardSkillInfoResponse> {
        const url = SERVER_HOST + "/persons/hard_skills";
        return ServerApiHelper.makeGetRequest<FindPersonHardSkillInfoResponse>({ person_id: personId }, url);
    }
}
