export class ReviewInfo {
    public reviewerName: string;
    public specializationDetail: string;
    public reviewDetails: string;
}

export class ReviewsVM {

    // Constructor

    public constructor() {
        this._reviews = new Array(3);

        this._reviews[0] = new ReviewInfo();
        this._reviews[0].reviewerName = "Сидорова Ксения";
        this._reviews[0].specializationDetail = "Лингвистика, переводчик";
        this._reviews[0].reviewDetails = "Текст отзыва, может быть достаточно большой";

        this._reviews[1] = new ReviewInfo();
        this._reviews[1].reviewerName = "Сидорова Ксения";
        this._reviews[1].specializationDetail = "Лингвистика, переводчик";
        this._reviews[1].reviewDetails = "Текст отзыва, может быть достаточно большой";

        this._reviews[2] = new ReviewInfo();
        this._reviews[2].reviewerName = "Сидорова Ксения";
        this._reviews[2].specializationDetail = "Лингвистика, переводчик";
        this._reviews[2].reviewDetails = "Текст отзыва, может быть достаточно большой";

        this.canShowMoreReviews = true;
    }

    // Public properties

    public get reviews(): ReviewInfo[] {
        return this._reviews;
    }

    public canShowMoreReviews: boolean;

    // Public methods

    public showMore(): void {
        // TODO:
    }

    private _reviews: ReviewInfo[];
}
