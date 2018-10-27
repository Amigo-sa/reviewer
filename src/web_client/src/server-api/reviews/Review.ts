/**
 * Review
 * - reviewer_id: id пользователя который оставил отзыв
 * - subject_id: Специализация пользователя на которого оставили отзыв
 * - topic: Заголовок
 * - description: Сообщение
 * - value: float Оценка от 0 до 100
 */

export default class Review {
    // tslint:disable-next-line:variable-name
    public reviewer_id: string;
    // tslint:disable-next-line:variable-name
    public subject_id: string;
    public topic: string;
    public description: string;
    public value: number;
}
