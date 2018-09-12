front-end app

axios.defaults.headers.post["X-App-Name"] = "Reiviewer";
export const user = {
    auth: (username, password) => {
        //console.log( AUTHENTICATE);
        return axios({
            method: 'post',
            url: AUTHENTICATE,
            withCredentials: true,
            data: {
                arg0: username,
                arg1: password
            }
        });
    },

    get: () => {
        return axios({
            method: 'post',
            url: GET_CURRENT_USER,
            withCredentials: true,
            data: {}
        });
    },

    findUsers: str => {
        return axios({
            method: 'post',
            url: FIND_USERS,
            withCredentials: true,
            data: {
                arg0: str
            }
        });
    },

    getSetting: () => {
        return axios({
            method: 'post',
            url: GET_USER_SETTING,
            withCredentials: true,
            data: {}
        });
    },

    logout: () => {
        return axios({
            method: 'post',
            url: LOGOUT,
            withCredentials: true,
            data: {}
        });
    }
};


