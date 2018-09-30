
// // /*

// // // import RegistrationApi from "../server-api/registration/RegistrationApi";
// // // import UserLoginRequest from "../server-api/registration/UserLoginRequest";
// // // import ErrorCodes from "../server-api/ErrorCodes";
// // // import { IUserData } from "../stores/AuthStore";

// // // const auth = {
// // //     login: (phone: string, password: string) => {
// // //         return RegistrationApi.userLogin(new UserLoginRequest(phone, password));
// // //     },

// // //     get: ( user?: IUserData) => {
// // //         if ( user && user.session_id && user.uid ) {
// // //             // TODO send request to get user
// // //             const headers = new Object();
// // //             headers["Authorization"] = "Bearer " + user.session_id;
// // //             RegistrationApi.getAllProfiles(headers).then((data) => { console.log("Persons", data); });

// // //             const me = RegistrationApi.getProfile(headers, user.uid).then((data) =>
// // // { console.log("Person", data); });
// // //             console.log("Person", me);
// // //             return Promise.resolve("Ура получили данные");
// // //         }
// // //         else {
// // //             return Promise.reject(ErrorCodes.AUTHORIZATION_ERROR);
// // //         }
// // //     },
// // // };

// // // export default auth;

// // import RegistrationApi from "../server-api/registration/RegistrationApi";
// // import UserLoginRequest from "../server-api/registration/UserLoginRequest";
// // import { IUserData } from "../stores/AuthStore";

// // const auth = {
// //     login: (phone: string, password: string) => {
// //         return RegistrationApi.userLogin(new UserLoginRequest(phone, password));
// //     },

// //     get: (user?: IUserData): Promise<IUserData | null> => {
// //         if (user && user.session_id && user.uid) {
// //             // TODO send request to get user
// //             const headers = new Object();
// //             headers["Authorization"] = "Bearer " + user.session_id;
// //             RegistrationApi.getAllProfiles(headers).then((data) => { console.log("Persons", data); });

// //             const me = RegistrationApi.getProfile(headers, user.uid).then((data)
// // => { console.log("Person", data); });
// //             console.log("Person", me);
// //             // TODO: send really user
// //             return Promise.resolve(null);
// //         }
// //         else {
// //             return Promise.reject(new Error("Authorization error"));
// //         }
// //     },
// // };

// // export default auth;

// // import { action, observable } from "mobx";
// // import auth from "../agent/auth";
// // import UserLoginResponse from "../server-api/registration/UserLoginResponse";

// // export interface IUserData {
// //     phone: string;
// //     session_id?: string;
// //     uid?: string;
// //     data?: object;
// // }

// // export class AuthStore {
// //     @observable public isAuth: boolean = false;

// //     @observable
// //     public user: IUserData = {
// //         phone: "",
// //         session_id: undefined,
// //         uid: undefined,
// //         data: undefined,
// //     };

// //     constructor() {
// //         console.log("Construct AuthStore");
// //     }

// //     @action
// //     public setPhone(phone: string) {
// //         this.user.phone = phone;
// //     }

// //     @action public reset() {
// //         // this.user = null;
// //     }

// //     @action
// //     public authenticate(phone: string, password: string) {
// //         const me = this;
// //         return auth.login(phone, password)
// //             .then((responce: UserLoginResponse) => { this.setUser(responce); })
// //             .then(() => me.getCurrentUser(true))
// //             .then(action(() => { this.setPhone(phone); this.isAuth = true; }))
// //             .catch((err) => { console.error("Authenticate", err); });
// //     }

// //     @action public register() {
// //         console.log("Register");
// //     }

// //     @action public logout() {
// //         this.setToken("");
// //         return Promise.resolve();
// //     }

// //     @action
// //     protected setUser(responce: UserLoginResponse) {
// //         this.setToken(responce.session_id);
// //         this.user.uid = responce.person_id;
// //     }

// //     @action
// //     protected setToken(token?: string) {
// //         this.user.session_id = token;
// //     }

// //     @action
// //     public tryAuthenticate() {
// //         return this.getCurrentUser()
// //             .then(action(() => { this.isAuth = true; }))
// //             .catch((err: object) => { console.error("Authenticate false"); throw err; });
// //     }

// //     protected getCurrentUser(force?: boolean): Promise<IUserData | null> {
// //         return !force && this.user && this.isAuth
// //             ? Promise.resolve(this.user)
// //             : auth.get(this.user);

// //         // return Promise.resolve(this.user);
// //     }
// // }
// // const authStore = new AuthStore();
// // export default authStore;

// // // import UserLoginRequest from "./UserLoginRequest";
// // // import UserLoginResponse from "./UserLoginResponse";
// // // import ServerApiHelper from "../ServerApiHelper";
// // // import { SERVER_HOST } from "src/constants";

// // // export default class RegistrationApi {

// // //     public static userLogin(request: UserLoginRequest): Promise<UserLoginResponse> {
// // //         return ServerApiHelper.makePostRequest<UserLoginResponse>(request, SERVER_HOST + "/user_login");
// // //     }
// // // }

// // import UserLoginRequest from "./UserLoginRequest";
// // import UserLoginResponse from "./UserLoginResponse";
// // import ServerApiHelper from "../ServerApiHelper";
// // import { SERVER_HOST } from "src/constants";
// // import UserProfileResponce from "./UserProfileResponce";

// // export default class RegistrationApi {

// //     public static userLogin(request: UserLoginRequest): Promise<UserLoginResponse> {
// //         return ServerApiHelper.makePostRequest<UserLoginResponse>(SERVER_HOST + "/user_login", { request });
// //     }

// //     // TODO: move to Persons class
// //     public static getProfile(headers: object, uid: string): Promise<UserProfileResponce> {
// //         return ServerApiHelper.makeGetRequest<UserProfileResponce>(SERVER_HOST + "/persons/" + uid, { headers });
// //     }

// //     // TODO: move to Persons model
// //     public static getAllProfiles(headers: object): Promise<UserProfileResponce> {
// //         return ServerApiHelper.makeGetRequest<UserProfileResponce>(SERVER_HOST + "/persons", { headers });
// //     }
// // }

// // // //  Шат
// // // // ле
// // // // МИ
// // // // specializationStudent
// // // // group_id{{group_id}}
// // // // department_id{{department_id}}
// // // // organization_id{{organization_id}}
// // // // query_limit10
// // // // query_start0

// // // export default class FindPersonsRequest {
// // //     public constructor FindPersonsRequest() {

// // //     }

// // //     public surname: string;
// // //     // tslint:disable-next-line:variable-name
// // //     public first_name: string;
// // //     public middle_name: string;
// // //     public specialization: string;
// // // }

// // import { action, observable } from "mobx";
// // import auth from "../agent/auth";
// // import UserLoginResponse from "../server-api/registration/UserLoginResponse";

// // export interface IUserData {
// //     phone: string;
// //     session_id?: string;
// //     uid?: string;
// //     data?: object;
// // }

// // export class AuthStore {
// //     @observable public isAuth: boolean = false;

// //     @observable
// //     public user: IUserData = {
// //         phone: "",
// //         session_id: undefined,
// //         uid: undefined,
// //         data: undefined,
// //     };

// //     constructor() {
// //         console.log("Construct AuthStore");
// //     }

// //     @action
// //     public setPhone(phone: string) {
// //         this.user.phone = phone;
// //     }

// //     @action public reset() {
// //         // this.user = null;
// //     }

// //     @action
// //     public authenticate(phone: string, password: string) {
// //         const me = this;
// //         return auth.login(phone, password)
// //             .then((responce: UserLoginResponse) => { this.setUser(responce); })
// //             .then(() => me.getCurrentUser(true))
// //             .then(action(() => { this.setPhone(phone); this.isAuth = true; }))
// //             .catch((err) => { console.error("Authenticate", err); });
// //     }

// //     @action public register() {
// //         console.log("Register");
// //     }

// //     @action public logout() {
// //         this.setToken("");
// //         return Promise.resolve();
// //     }

// //     @action
// //     protected setUser(responce: UserLoginResponse) {
// //         this.setToken(responce.session_id);
// //         this.user.uid = responce.person_id;
// //     }

// //     @action
// //     protected setToken(token?: string) {
// //         this.user.session_id = token;
// //     }

// //     @action
// //     public tryAuthenticate() {
// //         return this.getCurrentUser()
// //             .then(action(() => { this.isAuth = true; }))
// //             .catch((err: object) => { console.error("Authenticate false"); throw err; });
// //     }

// //     protected getCurrentUser(force?: boolean): Promise<IUserData | null> {
// //         return !force && this.user && this.isAuth
// //             ? Promise.resolve(this.user)
// //             : auth.get(this.user);

// //         // return Promise.resolve(this.user);
// //     }
// // }
// // const authStore = new AuthStore();
// // export default authStore;

// // // import axios, { AxiosResponse } from "axios";
// // // import Request from "./Request";

// // // /**
// // //  * Enumeration defining HTTP request methods.
// // //  */
// // // const enum HttpRequestMethod {
// // //     GET = "get",
// // //     POST = "post",
// // //     DELETE = "delete",
// // // }

// // // /**
// // //  * Contains help methods for work with server api.
// // //  */
// // // export default class ServerApiHelper {

// // //     /**
// // //      * Default value of HTTP request timeout in milliseconds.
// // //      */
// // //     private static DEFAULT_TIMEOUT: number = 1 * 60 * 1000;

// // //     /**
// // //      * Makes HTTP POST request to specific url.
// // //      * @param request object contains data which need to send to server.
// // //      * @param url server endpoint
// // //      * @param timeout timeout value
// // //      */
// // //     public static makePostRequest<Response>(request: object,
// // //                                             url: string,
// // //                                             timeout = ServerApiHelper.DEFAULT_TIMEOUT): Promise<Response> {
// // //         // make request with needed arguments
// // //         return ServerApiHelper._makeRequest(request, url, HttpRequestMethod.POST, timeout);
// // //     }

// // //     /**
// // //      * Makes HTTP GET request to specific url.
// // //      * @param request object contains data which need to send to server.
// // //      * @param url server endpoint
// // //      * @param timeout timeout value
// // //      */
// // //     public static makeGetRequest<Response>(request: object,
// // //                                            url: string,
// // //                                            timeout = ServerApiHelper.DEFAULT_TIMEOUT): Promise<Response> {
// // //         // make request with needed arguments
// // //         return ServerApiHelper._makeRequest(request, url, HttpRequestMethod.GET, timeout);
// // //     }

// // //     /**
// // //      * Makes HTTP DELETE request to specific url.
// // //      * @param request object contains data which need to send to server.
// // //      * @param url server endpoint
// // //      * @param timeout timeout value
// // //      */
// // //     public static makeDeleteRequest<Response>(request: object,
// // //                                               url: string,
// // //                                               timeout = ServerApiHelper.DEFAULT_TIMEOUT): Promise<Response> {
// // //         // make request with needed arguments
// // //         return ServerApiHelper._makeRequest(request, url, HttpRequestMethod.DELETE, timeout);
// // //     }

// // //     /**
// // //      * Makes request to server.
// // //      */
// // //     private static _makeRequest<Response>(request: object,
// // //                                           url: string,
// // //                                           method: string,
// // //                                           timeout: number): Promise<Response> {
// // //         // create intial values of request data
// // //         let requestData: object | /*undefined |*/ null = request;
// // //         let requestUrl = url;

// // //         // update url and request data for GET request method
// // //         if (method === HttpRequestMethod.GET) {
// // //             // update url, add propreties from request object
// // //             requestUrl = ServerApiHelper._addVariablesToUrl(url, request);
// // //             // use null request data
// // //             requestData = null;
// // //         }

// // //         // if in request there is auth token, then create header with it's info
// // //         // if in request there is auth token, then create header with it's info
// // //         const headers = new Object();
// // //         if (request instanceof Request) {
// // //             headers["Authorization"] = "Bearer " + (request as Request).authorizationToken;
// // //         }

// // //         // create promise base on Axios http request
// // //         const result = new Promise<Response>((resolve, reject) => {
// // //             axios({
// // //                 method,
// // //                 url: requestUrl,
// // //                 data: requestData,
// // //                 timeout,
// // //                 headers,
// // //             }).then((response: AxiosResponse<any>) => {
// // //                 resolve(response.data);
// // //             }, (reason: any) => {
// // //                 reject(reason);
// // //             });
// // //         });

// // //         return result;
// // //     }

// // //     /**
// // //      * Converts url variables to string
// // //      * @param urlVariables object with url variables.
// // //      */
// // //     private static _convertUrlVariablesToString(urlVariables: object): string {
// // //         return Object.keys(urlVariables)
// // //             .map((k) => `${k}=${urlVariables[k]}`)
// // //             .join("&");
// // //     }

// // //     /**
// // //      * Adds url variables to url.
// // //      * @param url initial url value
// // //      * @param urlVariables url variables
// // //      */
// // //     private static _addVariablesToUrl(url: string, urlVariables: object/* | undefined | null*/): string {
// // //         let result: string = url;

// // //         // add url variables, if need
// // //         if (/*urlVariables && */Object.keys(urlVariables).length > 0) {
// // //             // @ts-ignore compiler doesn't find that variable uses in template literal
// // //             const variables: string = this._convertUrlVariablesToString(urlVariables);
// // //             // @ts-ignore
// // //             result = "${url}?${variables}";
// // //         }

// // //         return result;
// // //     }

// // // }

// // import axios, { AxiosResponse } from "axios";

// // /**
// //  * Enumeration defining HTTP request methods.
// //  */
// // const enum HttpRequestMethod {
// //     GET = "get",
// //     POST = "post",
// //     DELETE = "delete",
// // }

// // export interface IRequestConfig {
// //     request?: object;
// //     timeout?: number;
// //     headers?: object;
// // }

// // /**
// //  * Contains help methods for work with server api.
// //  */
// // export default class ServerApiHelper {

// //     /**
// //      * Default value of HTTP request timeout in milliseconds.
// //      */
// //     private static DEFAULT_TIMEOUT: number = 1 * 60 * 1000;

// //     /**
// //      * Makes HTTP POST request to specific url.
// //      * @param request object contains data which need to send to server.
// //      * @param url server endpoint
// //      * @param timeout timeout value
// //      */
// //     public static makePostRequest<Response>(url: string, config: IRequestConfig): Promise<Response> {
// //         // make request with needed arguments
// //         return ServerApiHelper._makeRequest(HttpRequestMethod.POST,
// //             url,
// //             config.request,
// //             config.timeout || ServerApiHelper.DEFAULT_TIMEOUT,
// //             config.headers);
// //     }

// //     /**
// //      * Makes HTTP GET request to specific url.
// //      * @param request object contains data which need to send to server.
// //      * @param url server endpoint
// //      * @param timeout timeout value
// //      */
// //     public static makeGetRequest<Response>(url: string, config: IRequestConfig): Promise<Response> {
// //         // make request with needed arguments
// //         return ServerApiHelper._makeRequest(HttpRequestMethod.GET,
// //             url,
// //             config.request,
// //             config.timeout || ServerApiHelper.DEFAULT_TIMEOUT,
// //             config.headers);
// //     }

// //     /**
// //      * Makes HTTP DELETE request to specific url.
// //      * @param request object contains data which need to send to server.
// //      * @param url server endpoint
// //      * @param timeout timeout value
// //      */
// //     public static makeDeleteRequest<Response>(url: string,
// //                                               request: object,
// //                                               timeout = ServerApiHelper.DEFAULT_TIMEOUT,
// //                                               headers?: object): Promise<Response> {
// //         // make request with needed arguments
// //         return ServerApiHelper._makeRequest(url, HttpRequestMethod.DELETE, request, timeout, headers);
// //     }

// //     /**
// //      * Makes request to server.
// //      */
// //     private static _makeRequest<Response>(method: string,
// //                                           url: string,
// //                                           request?: object,
// //                                           timeout?: number,
// //                                           headers?: object): Promise<Response> {
// //         // create intial values of request data
// //         let requestData: object | undefined | null = request;
// //         let requestUrl = url;

// //         // update url and request data for GET request method
// //         if (method === HttpRequestMethod.GET) {
// //             // update url, add propreties from request object
// //             requestUrl = ServerApiHelper._addVariablesToUrl(url, request);
// //             // use null request data
// //             requestData = null;
// //         }

// //         // if in request there is auth token, then create header with it's info
// //         /*
// //         headers = new Object();
// //         if (headers instanceof Headers) {
// //             headers["Authorization"] = "Bearer " + (headers as Headers).authorizationToken;
// //         }
// //         */

// //         // create promise base on Axios http request
// //         const result = new Promise<Response>((resolve, reject) => {
// //             axios({
// //                 method,
// //                 url: requestUrl,
// //                 data: requestData,
// //                 timeout,
// //                 headers,
// //             }).then((response: AxiosResponse<any>) => {
// //                 resolve(response.data);
// //             }, (reason: any) => {
// //                 reject(reason);
// //             });
// //         });

// //         return result;
// //     }

// //     /**
// //      * Converts url variables to string
// //      * @param urlVariables object with url variables.
// //      */
// //     private static _convertUrlVariablesToString(urlVariables: object): string {
// //         return Object.keys(urlVariables)
// //             .map((k) => `${k}=${urlVariables[k]}`)
// //             .join("&");
// //     }

// //     /**
// //      * Adds url variables to url.
// //      * @param url initial url value
// //      * @param urlVariables url variables
// //      */
// //     private static _addVariablesToUrl(url: string, urlVariables: object | undefined | null): string {
// //         let result: string = url;

// //         // add url variables, if need
// //         if (urlVariables && Object.keys(urlVariables).length > 0) {
// //             // @ts-ignore compiler doesn't find that variable uses in template literal
// //             const variables: string = this._convertUrlVariablesToString(urlVariables);
// //             // @ts-ignore
// //             result = "${url}?${variables}";
// //         }

// //         return result;
// //     }

// // }

// // */

// import { action, observable } from "mobx";
// import auth from "../agent/auth";
// import UserLoginResponse from "../server-api/registration/UserLoginResponse";

// export class UserInfo {
//     public phone: string;
//     public sessionId?: string;
//     public personalId?: string;
// }

// /**
//  * AuthStore class.
//  * Contains functionality relative to authorization process: login, logout,
//  * get info about current user, etc.
//  */
// export class AuthStore {
//     @observable public isAuth: boolean = false;

//     @observable
//     public user: IUserData = {
//         phone: "",
//         session_id: undefined,
//         uid: undefined,
//         data: undefined,
//     };

//     constructor() {
//         console.log("Construct AuthStore");
//     }

//     @action
//     public setPhone(phone: string) {
//         this.user.phone = phone;
//     }

//     @action public reset() {
//         // this.user = null;
//     }

//     @action
//     public authenticate(phone: string, password: string) {
//         return auth.login(phone, password)
//             .then((responce: UserLoginResponse) => { this.setUser(responce); })
//             .then(() => { this.getCurrentUser(true).catch((err) => { console.error("Authenticate 1", err); }); })
//             .then(action(() => { this.setPhone(phone); this.isAuth = true; }))
//             .catch((err) => { console.error("Authenticate", err); });
//     }

//     @action public register() {
//         console.log("Register");
//     }

//     @action public logout() {
//         this.setToken("");
//         return Promise.resolve();
//     }

//     @action
//     protected setUser(responce: UserLoginResponse) {
//         this.setToken(responce.session_id);
//         this.user.uid = responce.person_id;
//     }

//     @action
//     protected setToken(token?: string) {
//         this.user.session_id = token;
//     }

//     @action
//     public tryAuthenticate() {
//         return this.getCurrentUser()
//             .then(action(() => { this.isAuth = true; }))
//             .catch((err: object) => { console.error("Authenticate false"); throw err; });
//     }

//     protected getCurrentUser(force?: boolean): Promise<any> {
//         return !force && this.user && this.isAuth
//             ? Promise.resolve(this.user)
//             : auth.get(this.user);

//         // return Promise.resolve(this.user);
//     }

//     // Private fields

// }
// const authStore = new AuthStore();
// export default authStore;
