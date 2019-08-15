/**
 * 
 * 
 *  XMLHttpRequest
 * 
 * */

// Get History 

function ajaxGet() {
  var getRequest = new XMLHttpRequest();
  var docURI = document.documentURI
  var endpoint = docURI.split('/')
  var endpoint = endpoint[endpoint.length - 1].replace(/-/g, '/')
  var information = document.querySelector('select').value.split(' ')
  var selectionDate = information[information.length - 1]
  if (endpoint != selectionDate) {
    if (endpoint != '' && information.length != 3) {
      ajaxGetLogic(getRequest, information)
    }
  }
}

function ajaxGetLogic(getRequest, information) {
  var information = document.querySelector('select').value.split(' ')
  if (information.length == 1 || information.length == 3) {
    getRequest.open("GET", '/', true)
    getRequest.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
        window.location = '/'
      }
    }
  }
  else {
    let date = information[information.length - 1]
    let url = `/${date.replace(/\//g, '-')}`
    getRequest.open("GET", url, true);
    getRequest.onreadystatechange = function () {
      if (this.readyState === 4 && this.status === 200) {
        window.location = `${url}`
      }
    }
  }
  getRequest.send()
}
