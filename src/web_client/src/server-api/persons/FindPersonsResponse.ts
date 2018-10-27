import Person from "./Person";
import Response from "src/server-api/Response";

export default class FindPersonsResponse extends Response {
    public length: number;
    public list?: Person[];
}
