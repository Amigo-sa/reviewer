/**
 * Review
 */
export default class Review {
    /**
     * id пользователя который оставил отзыв
     */
    // tslint:disable-next-line:variable-name
    public reviewer_id: string;

    /**
     * Специализация пользователя на которого оставили отзыв
     */
    // tslint:disable-next-line:variable-name
    public subject_id: string;

    /**
     * Заголовок
     */
    public topic: string;

    /**
     * Сообщение
     */
    public description: string;

    /**
     * Оценка от 0 до 100
     */
    public value: number;
}
