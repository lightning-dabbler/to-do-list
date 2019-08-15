/**
 * 
 * 
 *  XMLHttpRequest
 * 
 * */

 // Get History 

function ajaxGet() {
    var getRequest = new XMLHttpRequest();
    var information = document.querySelector('select').value.split(' ')
    if (information.length==1 || information.length==3){
        getRequest.open("GET", '/', true)
        getRequest.onreadystatechange = function () {
            if(this.readyState === 4 && this.status === 200) {
              window.location = '/'
            }
          }
    }
    else {
    let date = information[information.length - 1]
    let url = `/${date.replace(/\//g, '-')}`
    getRequest.open("GET", url, true);
    getRequest.onreadystatechange = function () {
        if(this.readyState === 4 && this.status === 200) {
          window.location = `${url}`
        }
      }
    }
    getRequest.send()
}