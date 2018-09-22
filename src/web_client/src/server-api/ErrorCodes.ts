
export default class ErrorCodes {
    // Common errors
    public static readonly SUCCESS: number = 0;
    public static readonly INCORRECT_FORMAT_OF_INPUT_DATA: number = 1;
    public static readonly INCORRECT_ACCESS_TO_DB: number = 2;
    public static readonly EMPTY_DB_RESPONCE: number = 3;

    // Authorization errors
    public static readonly AUTHORIZATION_ERROR: number = 4;
    public static readonly TOKEN_NOT_EXIST: number = 5;
    public static readonly INCORRECT_PHONE_NUMBER: number = 6;
    public static readonly LIMIT_OF_SMS_FOR_AUTHORIZATION: number = 7;
    public static readonly INCORRECT_AUTHORIZATION_CODE: number = 8;
    public static readonly TOKEN_EXPIRED: number = 9;
    public static readonly PERMISSION_ERROR: number = 10;
}
