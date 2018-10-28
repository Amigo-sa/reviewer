import { action, observable } from "mobx";
import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import Review from "src/server-api/reviews/Review";
import GetReviewInfoResponce from "src/server-api/reviews/GetReviewInfoResponce";

export class ReviewsStore {
    @observable
    public reviews: Review[] = [];

    @action
    public get(id: string, force = false): Promise<Review | undefined> {
        const review = this._peak(id);
        if (review && !force) {
            return Promise.resolve(review);
        }

        return ReviewsApi.getReview(id).then((response: GetReviewInfoResponce) => {
            if (response.result === 0) {
                this.reviews[id] = response.data;
                return review;
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
