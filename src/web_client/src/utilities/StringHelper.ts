/**
 * StringHelper class
 */
export class StringHelper {
    /**
     * Determines whether specified string is null or empty.
     */
    public static isNullOrEmpty(value: string): boolean {
        return (value == null || value.length === 0);
    }

    /**
     * Determines whether specified string is null, empty or contains only
     * white-space characters.
     */
    public static isNullOrWhiteSpace(value: string): boolean {
        return (value == null || value.trim().length === 0);
    }

    /**
     * Checks if two strings are equal.
     */
    public static areEqual(string1: string, string2: string, caseInsensitive: boolean = true): boolean {
        let result: boolean = false;
        if (string1 == null || string2 == null) {
            // If both strings are null then return true.
            if (string1 == null && string2 == null) {
                result = true;
            }
        } else {
            if (caseInsensitive) {
                result = string1.toLocaleUpperCase() === string2.toLocaleUpperCase();
            } else {
                result = string1 === string2;
            }
        }
        return result;
    }

    /**
     * Returns true if string ends with a specified suffix.
     * @param value - string to check
     * @param suffix - suffix
     * @param caseInsensitive - flag that show what is comparing: case sensitive or not.
     */
    public static endsWith(value: string, suffix: string, caseInsensitive: boolean = true): boolean {
        let result: boolean = false;

        const offset: number = value.length - suffix.length;
        if (offset >= 0) {
            const tail: string = value.substring(offset);
            result = StringHelper.areEqual(suffix, tail, caseInsensitive);
        }

        return result;
    }
}
