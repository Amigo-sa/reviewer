// TODO: need to use configuration dependent on constants, for debug and release.
export const SERVER_HOST: string = "http://151.248.120.88/develop";

export const REDIRECT_TO_LOGIN: string = "/";
export const REDIRECT_TO_AFTER_LOGIN: string = "/add-survey";

// TODO: use constant with {0}. Need to add substitute method to StringHelper
export const personUrlById = (id: string) => "/personal/" + id;
export const PERSON_URL: string = "/personal/{0}";
