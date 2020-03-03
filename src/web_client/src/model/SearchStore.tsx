import { action, observable } from "mobx";
import PersonsApi from "../server-api/persons/PersonsApi";
import Person from "../server-api/persons/Person";
import FindPersonsResponse from "../server-api/persons/FindPersonsResponse";
import FindPersonsRequest from "../server-api/persons/FindPersonsRequest";
import specializationsStore from "./SpecializationsStore";

export class SearchStore {
    @observable
    public resultList: Person[] = [];

    constructor() {
        console.debug("Construct SearchStore");
    }

    // #TODO парсер данных с сервера в клиентскую модель
    // #TODO - сделать полноценный поиск по параметрам
    @action
    public sendSeacrhPeople(findRequest: FindPersonsRequest) {
        // #TODO делаем запрос к серверу и получаем данные о пользователях и сохраняем в список
        return PersonsApi.findPersons(findRequest)
            .then(action((result: FindPersonsResponse) => {
                this.resultList = result.list || [];
            }))
            .catch((err: any) => console.log("Error Search", err));
    }

    // #TODO - получение специализаций пользователей при поиске(выпилить потом)
    public getPeopleSpecializations(): void {
        if (this.resultList) {
            this.resultList.forEach((el) => {
                const { id } = el;
                if (id) {
                    specializationsStore.get(id)
                        .then((list) => console.debug("Ok Search Spec", id, list))
                        .catch((err: any) => console.debug("Error Search Spec", err));
                }
            });
        }
    }

    @action public reset() {
        this.resultList = [];
    }
}

const searchStore = new SearchStore();
export default searchStore;
