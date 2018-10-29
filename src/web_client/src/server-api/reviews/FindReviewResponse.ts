import Response from "../Response";

interface ItemList {
    id: string;
}

export default class FindReviewResponse extends Response {
    public length: number;
    public list?: ItemList[];
}
