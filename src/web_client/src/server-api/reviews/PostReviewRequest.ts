/**
 * ReviewRequest
 * - topic: Заголовок
 * - description: Сообщение
 * - value: Оценка от 0 до 100
 */
export default class PostReviewRequest {
    public topic: string;
    public description: string;
    public value: number;

    public constructor(topic: string, description: string, value: number) {
        this.topic = topic;
        this.description = description;
        this.value = value;

    }
}
