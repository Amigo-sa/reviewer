// import ServerApiHelper from "../ServerApiHelper";
// import { SERVER_HOST } from "src/constants";
// import UserProfileResponce from "./UserProfileResponce";
import Person from "src/server-api/persons/Person";
import AddPersonResponse from "./AddPersonResponse";
import ServerApiHelper from "../ServerApiHelper";
import { SERVER_HOST } from "src/constants";
import FindPersonsRequest from "./FindPersonsRequest";
import FindPersonsResponse from "./FindPersonsResponse";
import Response from "../Response";
import GetPersonInfoResponse from "./GetPersonInfoResponse";

export default class PersonsApi {

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
        return ServerApiHelper.makeGetRequest<GetPersonInfoResponse>(null, url);
    }
}
