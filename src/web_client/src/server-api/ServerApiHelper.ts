import axios, { AxiosResponse } from "axios";
import { HttpRequestParameters } from "./HttpRequestParameters";

/**
 * Contains help methods for work with server api.
 */
export default class ServerApiHelper {
    /**
     * Makes request to server.
     */
    public static makeRequest<Request, Response>(request: Request,
                                                 url: string,
                                                 requestParameters: HttpRequestParameters): Promise<Response> {
        // create promise base on Axios http request
        const result = new Promise<Response>((resolve, reject) => {
            axios({
                method: requestParameters.getMethod(),
                url,
                data: request,
                timeout: requestParameters.getTimeout(),
            }).then((response: AxiosResponse<any>) => {
                resolve(response.data);
            }, (reason: any) => {
                reject(reason);
            });
        });

        return result;
    }
}
