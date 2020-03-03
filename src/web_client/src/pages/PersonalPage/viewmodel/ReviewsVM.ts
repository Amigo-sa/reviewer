import { computed, action, observable } from "mobx";
import FindReviewRequest from "src/server-api/reviews/FindReviewsRequest";
import ReviewsApi from "src/server-api/reviews/ReviewsApi";
import Review, { IPersonShort } from "src/server-api/reviews/Review";

export class ReviewInfo {
    public reviewId: string;
    public reviewerName: IPersonShort;
    public specializationDetail: string;
    public reviewDescription: string;
}

export class ReviewsVM {

    @computed
    public get loaded(): boolean {
        return this._loaded;
    }

    // Constructor

    public constructor() {
        this.canShowMoreReviews = true;
        this._loaded = false;
        this._reviews = [];
    }

    // Public methods

    @action
    public loadReviews(id: string): void {
        this._loaded = false;
        // формирование запроса поиска отзывов
        const findRequest = new FindReviewRequest();
        findRequest.person_id = id;
        findRequest.type = "specialization";
        const reviewsLoadInfo = ReviewsApi.findSpecializationReview(findRequest)
            .then((reviews) => {
                if (reviews.length && reviews.list) {
                    // ограничиваем вывод отзывов с конца
                    this._reviews = reviews.list
                        .reverse()
                        .slice(0, ReviewsVM.REVIEWS_COUNT_ON_PAGE).map((item) => this._parseReview(item));
                } else {
                    this.canShowMoreReviews = false;
                }
            }).catch(() => {
                this.canShowMoreReviews = false;
            });

        // Wait all parallel tasks
        Promise.all([reviewsLoadInfo]).then(() => {
            this._loaded = true;
        });
    }

    // Public properties

    public get reviews(): ReviewInfo[] {
        return this._reviews;
    }

    public canShowMoreReviews: boolean;

    // Public methods

    public showMore(): void {
        // TODO: load
    }
    private _parseReview(review: Review): ReviewInfo {
        const result = new ReviewInfo();
        result.reviewId = review.id;
        result.reviewerName = review.reviewer;
        result.reviewDescription = review.description;
        result.specializationDetail = review.subject.display_text;
        return result;
    }
    private static REVIEWS_COUNT_ON_PAGE: number = 3;
    @observable
    private _reviews: ReviewInfo[];
    @observable
    private _loaded: boolean;
}
