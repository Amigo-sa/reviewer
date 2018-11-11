import { action, observable } from "mobx";
import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import Review, { IPersonShort } from "src/server-api/reviews/Review";
import GetReviewInfoResponse from "src/server-api/reviews/GetReviewInfoResponse";
import PostReviewRequest from "src/server-api/reviews/PostReviewRequest";
import PostReviewResponse from "src/server-api/reviews/PostReviewResponse";
import FindReviewRequest from "src/server-api/reviews/FindReviewsRequest";

export class ReviewSpecializationInfo {
    public reviewerName: IPersonShort;
    public specializationDetail: string;
    public reviewTopic: string;
    public reviewDescription: string;
    public reviewScore: number;
    public reviewDate: Date;
    public isLoaded: boolean;
}

export class FindReviewsViews {
    public length: number;
    public list: ReviewSpecializationInfo[];
}

export class ReviewsStore {
    @observable
    public reviews: { [key: string]: ReviewSpecializationInfo } = {};

    @action
    public get(id: string, force = false): Promise<ReviewSpecializationInfo | undefined> {
        // #TODO продумать необходимость кэширования запросов
        const review = this._peak(id);
        if (review && !force) {
            return Promise.resolve(review);
        }

        return ReviewsApi.getReview(id).then((response: GetReviewInfoResponse) => {
            if (response.result === 0) {
                const data = this._parseReview(response.data);
                this.reviews[id] = data;
                return data;
            } else {
                throw undefined;
            }
        });
    }

    public getList(personId: string): Promise<FindReviewsViews | null> {
        const findRequest = new FindReviewRequest();
        // #TODO использовать для поиска либо только отзывов по специализациям или продумать
        findRequest.person_id = personId;
        findRequest.type = "specialization";
        return ReviewsApi.findSpecializationReview(findRequest)
            .then((reviews) => {
                if (reviews.length && reviews.list) {
                    const result = new FindReviewsViews();
                    result.length = reviews.length;
                    result.list = reviews.list.reverse().map((item) => this._parseReview(item));
                    return result;
                }
                return null;
            });
    }

    public addReview(specializationId: string,
                     topic: string,
                     description: string,
                     value: number): Promise<string | null> {
        const review = new PostReviewRequest(topic, description, value);
        return ReviewsApi.addReview(specializationId, review)
            .then((res: PostReviewResponse) => {
                console.log(`Create new review with id ${res.id}`);
                if (res.id) {
                    return Promise.resolve(res.id);
                }
                return Promise.reject("Error " + res.result);
            })
            .catch((err: any) => {
                console.log(`Something go wrong!`, err);
                return Promise.reject(err);
            });
    }

    private _peak(id: string): ReviewSpecializationInfo | undefined {
        const review = this.reviews[id];
        if (review) {
            return review;
        }
        return undefined;
    }

    private _parseReview(review: Review): ReviewSpecializationInfo {
        const result = new ReviewSpecializationInfo();
        result.reviewerName = review.reviewer;
        result.reviewTopic = review.topic;
        result.reviewDescription = review.description;
        result.reviewScore = review.value;
        result.specializationDetail = review.subject.display_text;
        result.reviewDate = new Date(review.date);
        result.isLoaded = true;

        return result;
    }

}

const reviewsStore = new ReviewsStore();
export default reviewsStore;
