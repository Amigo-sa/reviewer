import axios, { AxiosResponse } from "axios";

/**
 * Enumeration defining HTTP request methods.
 */
const enum HttpRequestMethod {
    GET = "get",
    POST = "post",
    DELETE = "delete",
}

export interface IRequestConfig {
    request?: object;
    timeout?: number;
    headers?: object;
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
     * @param timeout timeout value
     */
    public static makePostRequest<Response>(url: string, config: IRequestConfig): Promise<Response> {
        // make request with needed arguments
        return ServerApiHelper._makeRequest(HttpRequestMethod.POST,
                                            url,
                                            config.request,
                                            config.timeout || ServerApiHelper.DEFAULT_TIMEOUT,
                                            config.headers);
    }

    /**
     * Makes HTTP GET request to specific url.
     * @param request object contains data which need to send to server.
     * @param url server endpoint
     * @param timeout timeout value
     */
    public static makeGetRequest<Response>(url: string, config: IRequestConfig): Promise<Response> {
        // make request with needed arguments
        return ServerApiHelper._makeRequest(HttpRequestMethod.GET,
            url,
            config.request,
            config.timeout || ServerApiHelper.DEFAULT_TIMEOUT,
            config.headers);
    }

    /**
     * Makes HTTP DELETE request to specific url.
     * @param request object contains data which need to send to server.
     * @param url server endpoint
     * @param timeout timeout value
     */
    public static makeDeleteRequest<Response>(url: string,
                                              request: object,
                                              timeout = ServerApiHelper.DEFAULT_TIMEOUT,
                                              headers?: object): Promise<Response> {
        // make request with needed arguments
        return ServerApiHelper._makeRequest(url, HttpRequestMethod.DELETE, request, timeout, headers);
    }

    /**
     * Makes request to server.
     */
    private static _makeRequest<Response>(method: string,
                                          url: string,
                                          request?: object,
                                          timeout?: number,
                                          headers?: object): Promise<Response> {
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

        // if in request there is auth token, then create header with it's info
        /*
        headers = new Object();
        if (headers instanceof Headers) {
            headers["Authorization"] = "Bearer " + (headers as Headers).authorizationToken;
        }
        */

        // create promise base on Axios http request
        const result = new Promise<Response>((resolve, reject) => {
            axios({
                method,
                url: requestUrl,
                data: requestData,
                timeout,
                headers,
            }).then((response: AxiosResponse<any>) => {
                resolve(response.data);
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
            // @ts-ignore compiler doesn't find that variable uses in template literal
            const variables: string = this._convertUrlVariablesToString(urlVariables);
            // @ts-ignore
            result = "${url}?${variables}";
        }

        return result;
    }

}
