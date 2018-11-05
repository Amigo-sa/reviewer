import Response from "../Response";
import Person from "../persons/Person";

interface IReviewItemList {
    id: string;
    topic: string;
    description: string;
    value: string;
    reviewer: Person;
}

export default class FindReviewResponse extends Response {
    public length: number;
    public list?: IReviewItemList[];
}
