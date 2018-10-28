/**
 * FindReviewRequest
 * - reviewer_id: id пользователя который оставил отзыв
 * - subject_id: Специализация пользователя на которого оставили отзыв
 * - query_start: offset при поиске
 * - query_limit: Ограничение на количество записей за раз
 */

export default class FindReviewRequest {
    // tslint:disable-next-line:variable-name
    public reviewer_id?: string;
    // tslint:disable-next-line:variable-name
    public person_id?: string;
    // tslint:disable-next-line:variable-name
    public query_start?: number;
    // tslint:disable-next-line:variable-name
    public query_limit?: number;
}
