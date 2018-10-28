export class PersonSpecializationList {
    public list: PersonSpecialization[];
}

export default class PersonSpecialization {
    public id: string;
    // tslint:disable-next-line:variable-name
    public department_id: string;
    // tslint:disable-next-line:variable-name
    public is_active: boolean;
    public level: string;
    // tslint:disable-next-line:variable-name
    public specialization_type: string;
    // tslint:disable-next-line:variable-name
    public additional_details?: object;
}
