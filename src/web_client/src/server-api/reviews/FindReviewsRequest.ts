
export default class FindReviewRequest {
    /**
     * id пользователя который оставил отзыв
     */
    // tslint:disable-next-line:variable-name
    public reviewer_id?: string;

    /**
     * Специализация пользователя на которого оставили отзыв
     */
    // tslint:disable-next-line:variable-name
    public person_id?: string;

    /**
     * Тип отзыва по специализации/скиллам
     */
    public type?: string;

    /**
     * offset при поиске
     */
    // tslint:disable-next-line:variable-name
    public query_start?: number;

    /**
     * Ограничение на количество записей за раз
     */
    // tslint:disable-next-line:variable-name
    public query_limit?: number;
}
