
export interface IPersonShort {
    first_name: string;
    id: string;
    middle_name: string;
    surname: string;
}

export interface ISubjectItem {
    display_text: string;
    id: string;
}

/**
 * Review
 */
export default class Review {
    /**
     * id пользователя который оставил отзыв
     */
    public reviewer: IPersonShort;

    /**
     * Специализация пользователя на которого оставили отзыв
     */
    public subject: ISubjectItem;

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

    /**
     * Дата отзыва YYYY-mm-dd
     */
    public date: Date;
}
