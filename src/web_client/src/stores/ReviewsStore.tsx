import { action, observable } from "mobx";
import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import Review from "src/server-api/reviews/Review";
import GetReviewInfoResponse from "src/server-api/reviews/GetReviewInfoResponse";

export class ReviewsStore {
    @observable
    public reviews: { [key: string]: Review } = {};

    @action
    public get(id: string, force = false): Promise<Review | undefined> {
        // #TODO продумать необходимость кэширования запросов
        const review = this._peak(id);
        if (review && !force) {
            return Promise.resolve(review);
        }

        return ReviewsApi.getReview(id).then((response: GetReviewInfoResponse) => {
            if (response.result === 0) {
                this.reviews[id] = response.data;
                return response.data;
            }
            return undefined;
        });
    }

    private _peak(id: string): Review | undefined {
        const user = this.reviews[id];
        if (user) {
            return user;
        }
        return undefined;
    }

}

const reviewsStore = new ReviewsStore();
export default reviewsStore;
