import Person from "./Person";
import Response from "../Response";
export default class GetPersonInfoResponse extends Response {
    public data?: Person;
}
