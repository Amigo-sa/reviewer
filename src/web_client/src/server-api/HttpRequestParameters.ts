
import { HttpRequestMethod } from "src/server-api/HttpRequestMethod";

/**
 * Contains parameters used to send HTTP request.
 */
export class HttpRequestParameters {

    ///////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////////////////
    // Public constants

    /**
     * Default value of HTTP request timeout in milliseconds.
     */
    public static DEFAULT_TIMEOUT: number = 1 * 60 * 1000;

    /**
     * Default parameters for HTTP POST request.
     */
    public static DEFAULT_POST: HttpRequestParameters =
        new HttpRequestParameters(HttpRequestMethod.POST, HttpRequestParameters.DEFAULT_TIMEOUT);

    /**
     * Default parameters for HTTP GET request.
     */
    public static DEFAULT_GET: HttpRequestParameters =
        new HttpRequestParameters(HttpRequestMethod.GET, HttpRequestParameters.DEFAULT_TIMEOUT);

    /**
     * Default parameters for HTTP DELETE request.
     */
    public static DEFAULT_DELETE: HttpRequestParameters =
        new HttpRequestParameters(HttpRequestMethod.DELETE, HttpRequestParameters.DEFAULT_TIMEOUT);

    ///////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////////////////
    // Constructor

    /**
     * Creates an instance of HttpRequestParameters class.
     *
     * @param requestMethod - method of HTTP request.
     * @param timeout - timeout value in milliseconds.
     */
    constructor(requestMethod: HttpRequestMethod, timeout: number) {
        // TODO: add assertion of timeout, it must be > 0
        this._requestMethod = requestMethod;
        this._timeout = timeout;
    }

    ///////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////////////////
    // Public methods

    /**
     * Gets method of HTTP request.
     */
    public getMethod(): HttpRequestMethod {
        return this._requestMethod;
    }

    /**
     * Gets timeout value in milliseconds.
     */
    public getTimeout(): number {
        return this._timeout;
    }

    ///////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////////////////
    // Private fields

    /**
     * Method of HTTP request.
     */
    private _requestMethod: HttpRequestMethod;

    /**
     * Timeout value in milliseconds.
     */
    private _timeout: number /* int */;
}
