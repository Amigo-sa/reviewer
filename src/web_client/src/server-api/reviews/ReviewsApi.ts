import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetReviewInfoResponse from "./GetReviewInfoResponse";
import PostReviewResponse from "./PostReviewResponse";
import PostReviewRequest from "./PostReviewRequest";
import FindReviewRequest from "./FindReviewsRequest";
import FindReviewsResponse from "./FindReviewResponse";

export default class ReviewsApi {

    public static addReview(personSpecializationId: string, review: PostReviewRequest): Promise<PostReviewResponse> {
        const url = SERVER_HOST + "/specializations/" + personSpecializationId + "/reviews";
        // необходима авторизация добавляем true 3 параметром
        return ServerApiHelper.makePostRequest<PostReviewResponse>(review, url, true);
    }

    public static getReview(reviewId: string): Promise<GetReviewInfoResponse> {
        const url = SERVER_HOST + "/reviews/" + reviewId;
        return ServerApiHelper.makeGetRequest<GetReviewInfoResponse>(null, url);
    }

    public static findSpecializationReview(review: FindReviewRequest): Promise<FindReviewsResponse> {
        const url = SERVER_HOST + "/reviews";
        return ServerApiHelper.makeGetRequest<FindReviewsResponse>(review, url);
    }

}
