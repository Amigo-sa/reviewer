import Response from "../Response";
import Review from "./Review";

export default class FindReviewsResponse extends Response {
    public length: number;
    public list?: Review[];
}
