import { action, observable } from "mobx";

export interface ISearchData {
    fio: string;
    img: string;
    info: object;
}

export class SearchStore {
    @observable
    public resultList: ISearchData[] = [];

    constructor() {
        console.log("Construct SearchStore");
    }

    // #TODO - сделать полноценный поиск по параметрам
    @action
    public sendSeacrhPeople(surname: string) {
        // #TODO делаем запрос к серверу и получаем данные о пользователях и сохраняем в список
    }

    @action public reset() {
        this.resultList = [];
    }
}

const searchStore = new SearchStore();
export default searchStore;
