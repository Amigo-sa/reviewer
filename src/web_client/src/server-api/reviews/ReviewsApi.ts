import { SERVER_HOST } from "src/constants";
import ServerApiHelper from "../ServerApiHelper";
import GetReviewInfoResponce from "./GetReviewInfoResponce";
import PostReviewResponce from "./PostReviewResponce";
import PostReviewRequest from "./PostReviewRequest";
import FindReviewRequest from "./FindReviewsRequest";
import FindReviewResponce from "./FindReviewResponce";

export default class SkillsApi {

    public static addReview(personSpecializationId: string, review: PostReviewRequest): Promise<PostReviewResponce> {
        const url = SERVER_HOST + "specializations/" + personSpecializationId + "/reviews";
        // необходима авторизация добавляем true 3 параметром
        return ServerApiHelper.makePostRequest<PostReviewResponce>(review, url, true);
    }

    public static getReview(reviewId: string): Promise<GetReviewInfoResponce> {
        const url = SERVER_HOST + "reviews/" + reviewId;
        return ServerApiHelper.makeGetRequest<GetReviewInfoResponce>(null, url);
    }

    public static findReview(reviewId: FindReviewRequest): Promise<FindReviewResponce> {
        const url = SERVER_HOST + "reviews/" + reviewId;
        return ServerApiHelper.makeGetRequest<FindReviewResponce>(null, url);
    }

}
