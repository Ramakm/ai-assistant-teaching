import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'

// Create axios instance
const service = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// Request interceptor: carries the token field
service.interceptors.request.use(
  config => {
    // Do something before request is sent
    config.headers = config.headers || {}
    if (localStorage.getItem('token')) {
      config.headers.token = localStorage.getItem('token') || ''
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// Response interceptor
service.interceptors.response.use(
  response => {
    // What to do if the server response fails, because our real server might return code 20000 or 200
    if (response.status !== 201 && response.status != 200) {
      ElMessage({
        message: response.statusText || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (response.status === 404 || response.status === 50012 || response.status === 50014) {
        // To re-login
        ElMessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
          confirmButtonText: 'Re-Login',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          localStorage.dispatch('user/resetToken').then(() => {
            location.reload()
          })
        })
      }
      return Promise.reject(new Error('Server response error'))
    } else {
      // What to do if the server response succeeds
      return response
    }
  },
  error => {
    console.log('err' + error) // for debug
    ElMessage({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
