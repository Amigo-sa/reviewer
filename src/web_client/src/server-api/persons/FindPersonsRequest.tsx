
export default class FindPersonsRequest {
    public surname?: string;
    // tslint:disable-next-line:variable-name
    public first_name?: string;
    // tslint:disable-next-line:variable-name
    public middle_name?: string;
    public specialization?: string;
    // tslint:disable-next-line:variable-name
    public group_id?: string;
    // tslint:disable-next-line:variable-name
    public department_id?: string;
    // tslint:disable-next-line:variable-name
    public organization_id?: string;
    // tslint:disable-next-line:variable-name
    public query_limit: number;
    // tslint:disable-next-line:variable-name
    public query_start: number;
}
