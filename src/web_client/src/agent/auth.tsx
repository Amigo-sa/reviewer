import Axios from 'axios';

const API_ROOT = 'http://151.248.120.88/reviewer/';

const auth = {
    login: (phone: string, password: string) => {
        return Axios.post(API_ROOT + '/user_login', {
            data: {
                password: { password },
                phone_no: phone,
            },
            method: 'post',
            responseType: 'json'
        });
    },
    register: (phone: string, email: string, password: string) => {
        return Axios.post(API_ROOT + '/confirm_phone_no', {
            data: {
                phone_no: phone,
            },
            method: 'post',
            responseType: 'json'
        });
    }
};

export default auth;