import { computed } from "mobx";

export default class Person {
    public id: string;
    // tslint:disable-next-line:variable-name
    public first_name: string;
    // tslint:disable-next-line:variable-name
    public middle_name: string;
    public surname: string;
    // tslint:disable-next-line:variable-name
    public birth_date?: string;
    // tslint:disable-next-line:variable-name
    public phone_no?: string;
    // tslint:disable-next-line:variable-name
    public organization_name: string;
    public specialization: string;

    @computed
    get fio() {
        if (this.surname && this.first_name && this.middle_name) {
            return this.surname + " " + this.first_name + " " + this.middle_name;
        }
        return "";
    }
}
