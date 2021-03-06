import axios, { AxiosResponse } from "axios";
import ErrorCodes from "./ErrorCodes";

/**
 * Enumeration defining HTTP request methods.
 */
const enum HttpRequestMethod {
    GET = "get",
    POST = "post",
    DELETE = "delete",
}

/**
 * Contains help methods for work with server api.
 */
export default class ServerApiHelper {

    /**
     * Default value of HTTP request timeout in milliseconds.
     */
    private static DEFAULT_TIMEOUT: number = 1 * 60 * 1000;

    /**
     * Makes HTTP POST request to specific url.
     * @param request object contains data which need to send to server.
     * @param url server endpoint
     * @param isAuth indicates if need to use authorization info in request
     * @param timeout timeout value
     */
    public static makePostRequest<Response>(request: object | null,
                                            url: string,
                                            isAuth = false,
                                            timeout = ServerApiHelper.DEFAULT_TIMEOUT): Promise<Response> {
        // make request with needed arguments
        return ServerApiHelper._makeRequest(request, url, isAuth, HttpRequestMethod.POST, timeout);
    }

    /**
     * Makes HTTP GET request to specific url.
     * @param request object contains data which need to send to server.
     * @param url server endpoint
     * @param isAuth indicates if need to use authorization info in request
     * @param timeout timeout value
     */
    public static makeGetRequest<Response>(request: object | null,
                                           url: string,
                                           isAuth = false,
                                           timeout = ServerApiHelper.DEFAULT_TIMEOUT): Promise<Response> {
        // make request with needed arguments
        return ServerApiHelper._makeRequest(request, url, isAuth, HttpRequestMethod.GET, timeout);
    }

    /**
     * Makes HTTP DELETE request to specific url.
     * @param request object contains data which need to send to server.
     * @param url server endpoint
     * @param isAuth indicates if need to use authorization info in request
     * @param timeout timeout value
     */
    public static makeDeleteRequest<Response>(request: object | null,
                                              url: string,
                                              isAuth = false,
                                              timeout = ServerApiHelper.DEFAULT_TIMEOUT): Promise<Response> {
        // make request with needed arguments
        return ServerApiHelper._makeRequest(request, url, isAuth, HttpRequestMethod.DELETE, timeout);
    }

    /**
     * Makes request to server.
     */
    private static _makeRequest<Response>(request: object | null,
                                          url: string,
                                          isAuth: boolean,
                                          method: string,
                                          timeout: number): Promise<Response> {
        // create intial values of request data
        let requestData: object | undefined | null = request;
        let requestUrl = url;

        // update url and request data for GET request method
        if (method === HttpRequestMethod.GET) {
            // update url, add propreties from request object
            requestUrl = ServerApiHelper._addVariablesToUrl(url, request);
            // use null request data
            requestData = null;
        }

        // create headers
        const headers = new Object();
        if (isAuth) {
            const user = JSON.parse(localStorage.getItem("User") || "");
            if (user.token) {
                headers["Authorization"] = "Barrier " + user.token;
            }
        }
        // create promise base on Axios http request
        const result = new Promise<Response>((resolve, reject) => {
            axios({
                method,
                url: requestUrl,
                data: requestData,
                timeout,
                headers,
            }).then((response: AxiosResponse<any>) => {
                if (response.data.result === ErrorCodes.SUCCESS) {
                    resolve(response.data);
                } else {
                    reject(response.data);
                }
            }, (reason: any) => {
                reject(reason);
            });
        });

        return result;
    }

    /**
     * Converts url variables to string
     * @param urlVariables object with url variables.
     */
    private static _convertUrlVariablesToString(urlVariables: object): string {
        return Object.keys(urlVariables)
            .map((k) => `${k}=${urlVariables[k]}`)
            .join("&");
    }

    /**
     * Adds url variables to url.
     * @param url initial url value
     * @param urlVariables url variables
     */
    private static _addVariablesToUrl(url: string, urlVariables: object | undefined | null): string {
        let result: string = url;

        // add url variables, if need
        if (urlVariables && Object.keys(urlVariables).length > 0) {
            const variables: string = this._convertUrlVariablesToString(urlVariables);
            result = url + "?" + variables;
        }

        return result;
    }

}
